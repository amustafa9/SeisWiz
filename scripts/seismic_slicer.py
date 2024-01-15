from IPython.display import display, clear_output
from loading.load_segy import segy2npy
from visualization.slicer_utils import *
from pathlib import Path


# Class definition for seismic slice visualizer
class SeismicSlicer():
    def __init__(self, path_segy, fast_scan=True, **kwargs):
        """initializes class object by storing path to segy file"""

        # read segy file and extract seismic and other survey parameters
        seismic, ilines, xlines, samples = segy2npy(path_segy)

        self.seismic = seismic
        self.ilines = np.sort(ilines)
        self.xlines = np.sort(xlines)
        self.samples = np.sort(samples)
        self.std = seismic.std()
        self.horizon_flag = False  # Only visualize seismic

        # also plot horizon is horizon path provided
        if kwargs['horizon_file_path'] is not None:
            self.horizon_flag = True
            self.horizon_file_path = kwargs['horizon_file_path']

        # Use user-specified cmap if provided
        if kwargs['cmap'] is not None:
            self.cmap = kwargs['cmap']
        else:
            self.cmap = 'gray'  # use grayscale colormap otherwise

        # initialize initial frame values along all three directions
        self.current_frame_1 = 0
        self.current_frame_2 = 0
        self.current_frame_3 = 0
        self.clip_factor = 3
        
        # initialize gui and draw initial views
        self.initialize_slicer()

        # Attach the update function to the sliders' on_changed events
        self.frame_slider1.on_changed(self.update)
        self.frame_slider2.on_changed(self.update)
        self.frame_slider3.on_changed(self.update)
        self.clip_slider.on_changed(self.update)

        # show figure
        plt.show()
     
    def initialize_slicer(self):
        
        # Create initial figure
        fig, ax = plt.subplots(1, 2)
        plt.subplots_adjust(bottom=0.25)

        # initialize section view
        img1 = self.init_section_view(ax[0])

        # initialize horizon plot
        if self.horizon_flag:
            if Path(self.horizon_file_path).is_file():  # check if path is a single file or a directory of horizons
                self.picks = self.save_picks(self.horizon_file_path)
                self.horizon_plot = self.plot_horizon(img1, self.picks, Path(self.horizon_file_path).name)
            else:
                self.horizon_file_paths = list_files_in_directory(self.horizon_file_path)
                self.horizon_plots = []  # list to store matplotlib line2D artists for every horizon
                self.picks_all_hrzs = []  # class variable to store picks for all files
                for file in self.horizon_file_paths:
                    picks = self.save_picks(file)
                    self.horizon_plots.append(self.plot_horizon(img1, picks, Path(file).name))
                    self.picks_all_hrzs.append(picks)

        # initialize depth view
        img2 = self.init_depth_view(ax[1])
        
        # draw positional markers on sectional view
        crossline_marker, depth_marker = self.draw_positional_markers_section_view(img1)

        # draw positional markers on depth view
        inline_marker, crossline_marker_depth = self.draw_positional_markers_depth_view(img2)

        # Add sliders for interactive frame navigation along inline, crossline, and depth directions
        nil, nxl, nz = self.seismic.shape
        init_vals = (self.current_frame_1, self.current_frame_2, self.current_frame_3)
        frame_slider1, frame_slider2, frame_slider3 = create_section_sliders(nil, nxl, nz, init_vals)

        # create slider to apply clipping to seismic views
        clip_slider = create_clip_slider()

        self.fig = fig
        self.img1 = img1
        self.img2 = img2
        self.crossline_marker = crossline_marker
        self.depth_marker = depth_marker
        self.inline_marker = inline_marker
        self.crossline_marker_depth = crossline_marker_depth
        self.frame_slider1 = frame_slider1
        self.frame_slider2 = frame_slider2
        self.frame_slider3 = frame_slider3
        self.clip_slider = clip_slider

    def update(self, val):
        """update views based off user input to sliders"""

        # retrieve current values from sliders
        self.current_frame_1 = int(self.frame_slider1.val)
        self.current_frame_2 = int(self.frame_slider2.val)
        self.current_frame_3 = int(self.frame_slider3.val)
        self.clip_factor = int(self.clip_slider.val)

        # update inline/crossline view
        self.img1.set_array(plot_section_slices(self.seismic, self.current_frame_1, self.current_frame_2))

        # update horizon plot by extracting x/y picks to plot on section view
        if self.horizon_flag:
            if Path(self.horizon_file_path).is_file():  # if only one horizon file
                self.update_horizon_plot(self.picks, self.horizon_plot)
            else: # if multiple files
                for picks, artist in zip(self.picks_all_hrzs, self.horizon_plots):
                    self.update_horizon_plot(picks, artist)

        # update marker positions on inline/crossline view
        self.crossline_marker[0].set_ydata([self.samples[self.current_frame_3], self.samples[self.current_frame_3]])
        self.depth_marker[0].set_xdata([self.current_frame_2, self.current_frame_2])

        # update depth slice view
        self.img2.set_array(plot_depth_slice(self.seismic, self.current_frame_3))

        # update inline and crossline markers on depth view
        self.inline_marker[0].set_ydata([self.ilines[self.current_frame_1], self.ilines[self.current_frame_1]])
        self.crossline_marker_depth[0].set_xdata([self.xlines[self.current_frame_2], self.xlines[self.current_frame_2]])

        # show legend
        self.img1.axes.legend()

        # apply clipping to image views
        self.img1.set_clim(vmin=-self.clip_factor*self.std, vmax=self.clip_factor*self.std)
        self.img2.set_clim(vmin=-self.clip_factor * self.std, vmax=self.clip_factor * self.std)

        self.fig.canvas.draw_idle()
        clear_output(wait=True)
        display(self.fig)

    def init_section_view(self, ax):
        """function creates and populates an artist to show an image consisting
         of the stitched inline and crossline views through the volume"""

        # create inline/crossline view and set title
        img = ax.imshow(plot_section_slices(self.seismic, self.current_frame_1, self.current_frame_2),
                            extent=(0, self.seismic.shape[0]+self.seismic.shape[1], self.samples.max(), self.samples.min()),
                            cmap=self.cmap, vmin=-self.clip_factor*self.std, vmax=self.clip_factor*self.std, aspect='auto')

        ax.set_xticks([])
        ax.set_ylabel('Depth')
        ax.set_xlabel('Sample Position Laterally')
        img.axes.set_title('Inline\Crossline View')

        return img

    def init_depth_view(self, ax):
        """function creates and populates an artist to show an image consisting
         of the depth view through the volume"""

        # create depth slice view and set title
        img = ax.imshow(plot_depth_slice(self.seismic, self.current_frame_3),
                            extent=(self.xlines.min(), self.xlines.max(), self.ilines.max(), self.ilines.min()),
                            cmap=self.cmap, vmin=-3*self.std, vmax=3*self.std, aspect='auto')

        ax.set_xlabel('Crossline Numbers')
        ax.set_ylabel('Inline Numbers')
        img.axes.set_title('Depth View')

        return img

    def draw_positional_markers_section_view(self, section_view_ax):
        """function draws lines on the section view denoting the position of the current depth
        slice and crosslines

        Parameters:
            section_view_ax: matplotlib artist object
                matplotlib artist object showing the axes used to create the initial sectional view
        """

        # draw vertical line showing position of crossline
        crossline_marker = section_view_ax.axes.plot([0, self.seismic.shape[0] + self.seismic.shape[1] - 1],
                                          [self.samples[self.current_frame_3], self.samples[self.current_frame_3]],
                                          color='black')

        # draw horizontal line to denote depth marker
        depth_marker = section_view_ax.axes.plot([self.current_frame_2, self.current_frame_2],
                                      [self.samples.max(), self.samples.min()], color='black')

        return crossline_marker, depth_marker

    def draw_positional_markers_depth_view(self, depth_view_ax):
        """function draws lines on the depth view denoting the position of the current inline
        and crossline slices

        Parameters:
            depth_view_ax: matplotlib artist object
                matplotlib artist object showing the axes used to create the initial depth view
        """

        # draw horizontal line to show inline slice position
        inline_marker = depth_view_ax.axes.plot([self.xlines.min(), self.xlines.max()],
                                       [self.ilines[self.current_frame_1], self.ilines[self.current_frame_1]],
                                       color='black')

        # draw vertical line to show crossline position
        crossline_marker_depth = depth_view_ax.axes.plot([self.xlines[self.current_frame_2], self.xlines[self.current_frame_2]],
                                                [self.ilines[0], self.ilines[self.seismic.shape[0] - 1]], color='black')

        return inline_marker, crossline_marker_depth

    def save_picks(self, horizon_file_path):
        """function extracts columns from horizon text files and saves them as class variables to
        later be used for plotting picks"""

        # read horion picks file
        horizon_file = np.genfromtxt(horizon_file_path)

        # picks object to store columns
        picks = []

        # extract horizon picks
        picks.append(horizon_file[1:, 0].astype(int))
        picks.append(horizon_file[1:, 1].astype(int))
        picks.append(horizon_file[1:, 2].astype(int))

        return picks

    def plot_horizon(self, img, picks, filename):
        """plot horizon on section view on img object"""

        # extract horizon picks
        inline_picks = picks[0]
        xline_picks = picks[1]
        z_picks = picks[2]

        # extract x/y picks to plot on section view
        x_coords, y_coords = extract_section_picks(np.sort(self.ilines), np.sort(self.xlines), np.sort(self.samples),
                                                   inline_picks, xline_picks, z_picks, self.current_frame_1,
                                                   self.current_frame_2)

        # plot on img artist
        horizon_plot = img.axes.plot(x_coords, y_coords, label=filename)

        return horizon_plot

    def update_horizon_plot(self, picks, horizon_artist):
        """function updates horizon plot based on current inline/xline information"""

        # extract horizon picks
        inline_picks = picks[0]
        xline_picks = picks[1]
        z_picks = picks[2]

        # extract x/y picks to plot on section view
        x_coords, y_coords = extract_section_picks(np.sort(self.ilines), np.sort(self.xlines), np.sort(self.samples),
                                                   inline_picks, xline_picks, z_picks, self.current_frame_1,
                                                   self.current_frame_2)

        # update the horizon artist
        horizon_artist[0].set_xdata(x_coords)
        horizon_artist[0].set_ydata(y_coords)








