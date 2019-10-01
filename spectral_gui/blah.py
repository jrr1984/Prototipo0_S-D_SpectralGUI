import matplotlib.pyplot as plt
import mpld3
from datetime import datetime


class MousePositionDatePlugin(mpld3.plugins.PluginBase):
    """Plugin for displaying mouse position with a datetime x axis."""

    JAVASCRIPT = """
    mpld3.register_plugin("mousepositiondate", MousePositionDatePlugin);
    MousePositionDatePlugin.prototype = Object.create(mpld3.Plugin.prototype);
    MousePositionDatePlugin.prototype.constructor = MousePositionDatePlugin;
    MousePositionDatePlugin.prototype.requiredProps = [];
    MousePositionDatePlugin.prototype.defaultProps = {
    fontsize: 12,
    xfmt: "%Y-%m-%d %H:%M:%S",
    yfmt: ".3g"
    };
    function MousePositionDatePlugin(fig, props) {
    mpld3.Plugin.call(this, fig, props);
    }
    MousePositionDatePlugin.prototype.draw = function() {
    var fig = this.fig;
    var xfmt = d3.time.format(this.props.xfmt);
    var yfmt = d3.format(this.props.yfmt);
    var coords = fig.canvas.append("text").attr("class", "mpld3-coordinates").style("text-anchor", "end").style("font-size", this.props.fontsize).attr("x", this.fig.width - 5).attr("y", this.fig.height - 5);
    for (var i = 0; i < this.fig.axes.length; i++) {
      var update_coords = function() {
        var ax = fig.axes[i];
        return function() {
          var pos = d3.mouse(this);
          x = ax.xdom.invert(pos[0]);
          y = ax.ydom.invert(pos[1]);
          coords.text("(" + xfmt(x) + ", " + yfmt(y) + ")");
        };
      }();
      fig.axes[i].baseaxes.on("mousemove", update_coords).on("mouseout", function() {
        coords.text("");
      });
    }
    };
    """
    def __init__(self, fontsize=14, xfmt="%Y-%m-%d %H:%M:%S", yfmt=".3g"):
        self.dict_ = {"type": "mousepositiondate",
                      "fontsize": fontsize,
                      "xfmt": xfmt,
                      "yfmt": yfmt}


fig, ax = plt.subplots()

dates = [datetime(2015, 9, 10), datetime(2015, 9, 11), datetime(2015, 9, 12), datetime(2015, 9, 13)]
values = [2, 4, 6, 8]

points = plt.plot(dates, values, marker="o", markerfacecolor="none")

mpld3.plugins.connect(fig, MousePositionDatePlugin())

mpld3.save_html(fig, "./mpld3_mousepositiondateplugin.html")