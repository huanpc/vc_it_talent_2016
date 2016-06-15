import csv
from collections import deque
from nupic.algorithms import anomaly_likelihood
from abc import ABCMeta, abstractmethod

try:
    import matplotlib
    matplotlib.use('TKAgg')
    import matplotlib.pyplot as plt
    import matplotlib.gridspec as gridspec
    from matplotlib.dates import date2num, DateFormatter
except ImportError:
    pass

WINDOW = 300
HIGHLIGHT_ALPHA = 0.3
ANOMALY_HIGHLIGHT_COLOR = 'red'
WEEKEND_HIGHLIGHT_COLOR = 'yellow'
ANOMALY_THRESHOLD = 0.9


class NuPICOutput(object):

    __metaclass__ = ABCMeta

    def __init__(self, name):
        self.name = name
        self.anomaly_likelihood_helper = anomaly_likelihood.AnomalyLikelihood()

    @abstractmethod
    def write(self, timestamp, value, predicted, anomaly_score):
        pass

    @abstractmethod
    def close(self):
        pass


class NuPICFileOutput(NuPICOutput):

    def __init__(self, *args, **kwargs):
        super(NuPICFileOutput, self).__init__(*args, **kwargs)
        self.output_files = []
        self.output_writers = []
        self.line_count = 0
        header_row = [
            'timestamp',
            'value',
            'prediction',
            'anomaly_score',
            'anomaly_likelihood'
        ]

        output_file_name = "%s_out.csv" % self.name
        print "Preparing to output %s data to %s" % (self.name, output_file_name)
        self.output_file = open(output_file_name, 'w')
        self.output_writer = csv.writer(self.output_file)
        self.output_writer.writerow(header_row)

    def write(self, timestamp, value, predicted, anomaly_score):
        if timestamp is not None:
            anomaly_likelihood = self.anomaly_likelihood_helper.anomalyProbability(
                value, anomaly_score, timestamp
            )
        output_row = [
            timestamp, 
            value, 
            predicted, 
            anomaly_score, 
            anomaly_likelihood
        ]
        self.output_writer.writerow(output_row)
        self.line_count += 1

    def close(self):
        self.output_file.close()
        print "Done. Wrote %i data lines to %s." % (self.line_count, self.name)


def extract_weekend_highlights(dates):
    weekends_out = []
    weekend_search = [5, 6]
    weekend_start = None
    for i, date in enumerate(dates):
        if date.weekday() in weekend_search:
            if weekend_start is None:
                # Mark start of weekend
                weekend_start = i
        else:
            if weekend_start is not None:
                # Mark end of weekend
                weekends_out.append((
                    weekend_start, i, WEEKEND_HIGHLIGHT_COLOR, HIGHLIGHT_ALPHA
                ))
            weekend_start = None

    # Cap it off if we're still in the middle of a weekend
    if weekend_start is not None:
        weekends_out.append((
            weekend_start, len(
                dates)-1, WEEKEND_HIGHLIGHT_COLOR, HIGHLIGHT_ALPHA
        ))

    return weekends_out


def extract_anomaly_indices(anomaly_likelihood):
    anomalies_out = []
    anomaly_start = None
    for i, likelihood in enumerate(anomaly_likelihood):
        if likelihood >= ANOMALY_THRESHOLD:
            if anomaly_start is None:
                # Mark start of anomaly
                anomaly_start = i
        else:
            if anomaly_start is not None:
                # Mark end of anomaly
                anomalies_out.append((
                    anomaly_start,
                    i,
                    ANOMALY_HIGHLIGHT_COLOR,
                    HIGHLIGHT_ALPHA
                ))
                anomaly_start = None

    if anomaly_start is not None:
        anomalies_out.append((
            anomaly_start,
            len(anomaly_likelihood)-1,
            ANOMALY_HIGHLIGHT_COLOR,
            HIGHLIGHT_ALPHA
        ))

    return anomalies_out


class NuPICPlotOutput(NuPICOutput):

    def __init__(self, *args, **kwargs):
        super(NuPICPlotOutput, self).__init__(*args, **kwargs)
        # Turn matplotlib interactive mode on
        plt.ion()
        self.dates = []
        self.converted_dates = []
        self.value = []
        self.all_values = []
        self.predicted = []
        self.anomaly_score = []
        self.anomaly_likelihood = []
        self.actual_line = []
        self.predicted_line = []
        self.anomaly_score_line = []
        self.anomaly_likelihood_line = []
        self.lines_initialized = False
        self._char_highlights = []
        fig = plt.figure(figsize=(16, 10))
        gs = gridspec.GridSpec(2, 1, height_ratios=[3,  1])

        self._main_graph = fig.add_subplot(gs[0, 0])
        plt.title(self.name)
        plt.ylabel('Value')
        plt.xlabel('Date')

        self._anomaly_graph = fig.add_subplot(gs[1])

        plt.ylabel('Percentage')
        plt.xlabel('Date')

        # Maximizes window
        mng = plt.get_current_fig_manager()
        mng.resize(*mng.window.maxsize())

        plt.tight_layout()

    def initialize_lines(self, timestamp):
        print "initializing %s" % self.name
        anomaly_range(0.0, 1.0)
        self.dates = deque([timestamp] * WINDOW, maxlen=WINDOW)
        self.converted_dates = deque(
            [date2num(date) for date in self.dates],
            maxlen=WINDOW
        )
        self.value = deque([0.0] * WINDOW, maxlen=WINDOW)
        self.predicted = deque([0.0] * WINDOW, maxlen=WINDOW)
        self.anomaly_score = deque([0.0] * WINDOW, maxlen=WINDOW)
        self.anomaly_likelihood = deque([0.0] * WINDOW, maxlen=WINDOW)

        actual_plot, = self._main_graph.plot(self.dates, self.value)
        self.actual_line = actual_plot
        predicted_plot, = self._main_graph.plot(self.dates, self.predicted)
        self.predicted_line = predicted_plot
        self._main_graph.legend(tuple(['actual', 'predicted']), loc=3)

        anomaly_score_plot, = self._anomaly_graph.plot(
            self.dates, self.anomaly_score, 'm'
        )

        anomaly_score_plot.axes.set_ylim(anomaly_range)

        self.anomaly_score_line = anomaly_score_plot
        anomaly_likelihood_plot, = self._anomaly_graph.plot(
            self.dates, self.anomaly_score, 'r'
        )

        anomaly_likelihood_plot.axes.set_ylim(anomaly_range)
        self.anomaly_likelihood_line = anomaly_likelihood_plot
        self._anomaly_graph.legend(
            tuple(['anomaly score', 'anomaly likelihood']), loc=3
        )

        date_formatter = DateFormatter('%Y-%m-%d %H:%M:%S')
        self._main_graph.xaxis.set_major_formatter(date_formatter)
        self._anomaly_graph.xaxis.set_major_formatter(date_formatter)

        self._main_graph.relim()
        self._main_graph.autoscale_view(True, True, True)

        self.lines_initialized = True

    def highlight_chart(self, highlights, chart):
        for highlight in highlights:
            # Each highlight contains [start-index, stop-index, color alpha]
            self._chartHighlights.append(chart.axvspan(
                self.convertedDates[highlight[0]],
                self.convertedDates[highlight[1]],
                color=highlight[2],
                alpha=highlight[3]
            ))

    def write(self, timestamp, value, predicted, anomaly_score):
        if not self.lines_initialized:
            self.initialize_lines(timestamp)

        anomaly_likelihood = self.anomaly_likelihood_helper.anomalyProbability(
            value,
            anomaly_score,
            timestamp
        )

        self.dates.append(timestamp)
        self.converted_dates.append(date2num(timestamp))
        self.value.append(value)
        self.all_values.append(value)
        self.predicted.append(predicted)
        self.anomaly_score.append(anomaly_score)
        self.anomaly_likelihood.append(anomaly_likelihood)

        # Update the main chart area
        self.actual_line.set_xdata(self.converted_dates)
        self.actual_line.set_ydata(self.value)
        self.predicted_line.set_xdata(self.converted_dates)
        self.predicted_line.set_ydata(self.predicted)
        # Update anomaly chart data
        self.anomaly_score_line.set_xdata(self.converted_dates)
        self.anomaly_score_line.set_ydata(self.anomaly_score)
        self.anomaly_likelihood_line.set_xdata(self.converted_dates)
        self.anomaly_likelihood_line.set_ydata(self.anomaly_likelihood)

        # Remove previous highlighed regions
        for poly in self._char_highlights:
            poly.remove()
        self._char_highlights = []

        weekends = extract_weekend_highlights(self.dates)
        anomalies = extract_anomaly_indices(self.anomaly_likelihood)

        # Highlight weekends in main chart
        self.highlight_chart(weekends, self._main_graph)

        # Highlight anomalies in anomaly chart
        self.highlight_chart(anomalies, self._anomaly_graph)

        max_value = max(self.all_values)
        self._main_graph.relim()
        self._main_graph.axes.set_ylim(0, max_value + (max_value * 0.02))

        self._main_graph.relim()
        self._main_graph.autoscale_view(True, scaley=False)
        self._anomaly_graph.relim()
        self._anomaly_graph.autoscale_view(True, True, True)

        plt.draw()


    def close(self):
        plt.ioff()
        plt.show()


NuPICOutput.register(NuPICFileOutput)
NuPICOutput.register(NuPICPlotOutput)