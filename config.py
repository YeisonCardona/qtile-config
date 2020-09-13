from libqtile.config import Key, Screen, Group, Drag, Click
from libqtile.command import lazy
from libqtile import layout, bar, widget

import datetime
import time
import os
import random

HOME = os.path.expanduser("~/.config/qtile")

ARCHLOGO = os.path.join(HOME, "logo.png")
WALLPAPER = os.path.join(HOME, "wallpaper.png")
TERMINAL = "lxterminal"

VOLUME_MUTE = "amixer -q set Master toggle"
VOLUME_UP = "amixer sset Master 1%+ unmute"
VOLUME_DOWN = "amixer sset Master 1%- unmute"
TURN_OFF_MONITOR = "sleep 0.1; xset dpms force off"
BRIGHTNESS_DOWN = 'xbacklight -dec 10'
BRIGHTNESS_UP = 'xbacklight -inc 10'
AUDIO_NEXT = "playerctl next"
AUDIO_PREV = "playerctl previous"
AUDIO_PLAY = "playerctl play-pause"

mod = "mod4"

GROUPS = [("RaspberryPi4", "monadwide"),
          ("terminal", "bsp"),
          #("remote", "ratiotile"),
          #("development", "monadwide"),
          #("debug", "bsp"),
          #("files", "max"),
          # ("cnc", "monadtall"),
          #("bitcoin", "monadtall"),
          #("design", "monadtall"),
          #("music", "monadtall"),
          ]

COLORS = {

    'celeste': (
        "#00ccff",
        '#005a71',
        '#004455',
        '#000000',
        '#ff0066',
    ),

    'ambar': (
        "#ffcc00",
        '#806600',
        '#554400',
        '#000000',
        '#ff0066',
    ),

    'esmeralda': (
        "#00ffcc",
        '#008066',
        '#005544',
        '#000000',
        '#ff0066',
    ),

    'fucsia': (
        "#ff2a7f",
        '#aa0044',
        '#550022',
        '#000000',
        '#ff0066',
    ),

    'alma': (
        "#ffffff",
        '#cccccc',
        '#666666',
        '#000000',
        '#ff0066',
    ),

    'kawasaki': (
        "#00ff00",
        '#00aa00',
        '#005500',
        '#000000',
        '#ff0066',
    ),

    'raspberry': (

        '#c7053d',

        '#aa0044',
        '#550022',
        '#000000',
        '#ff0066',

    ),


    # 'red': (
    # "#ff0000",
    # '#d40000',
    # '#800000',
    # '#000000',
    # '#ff0066',
    # ),

}


# DEFAULT_THEME = 'raspberry'
DEFAULT_THEME = 'celeste'
THEME = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'theme')


########################################################################
class MyQtile:
    """"""

    # ----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        global WALLPAPER

        if os.path.exists(THEME):
            f = open(THEME, 'r')
            lines = f.read()
            f.close()
            os.remove(THEME)
            color = COLORS.get(lines.strip(), DEFAULT_THEME)
        else:
            color = COLORS[DEFAULT_THEME]

        self.theme = {
            "font-family": "Ubuntu Mono",

            "separator": color[0],
            "border-graph": color[0],
            "border": color[0],

            "foreground": color[0],
            "foreground-2nd": color[3],
            "alert": color[4],

            "graph-color": color[0],

            "panel-top": color[3],
            "panel-bottom": color[3],
            "panel-2nd": color[0],

            "primary": color[0],
            "primary-2nd": color[2],
            "inactive": color[1],
            "active": color[0],

            "border-width": 2,
            "border-width-active": 2,
            "size-lg": 15,
            "size-md": 13,
            "size-sm": 13,
            "size-xsm": 11,
            "rounded": False,
            "top-height": 27,
            "bottom-height": 15,
            "group-highlight": "line",

            "separator-padding": 10,

        }

        self.groups = [Group(i, layout=j) for i, j in GROUPS]
        self.keys = self.init_keys()
        self.layouts = self.init_layouts()
        self.widget_defaults = self.init_widgets()
        self.screens = self.init_screens()
        self.mouse = self.init_mouse()
        self.floating_layout = self.init_floating_layout()

        # if os.path.join(HOME, 'wallpappers', "default.jpg"):
        #WALLPAPER = os.path.join(HOME, 'wallpappers', "default.jpg")
        # else:
        self.set_art()

    # ----------------------------------------------------------------------

    @lazy.function
    def change_theme(qtile):
        """"""
        f = open(THEME, 'w')
        f.write(random.choice(list(COLORS.keys())))
        f.close()

    # ----------------------------------------------------------------------

    def set_art(self):
        """"""
        file = open(ARCHLOGO.replace(".png", '.svg'), 'r')
        logo = file.read()
        file.close()
        logo = logo.replace("#00ff00", self.theme['foreground-2nd'])
        logo = logo.replace("#ff0000", self.theme['panel-2nd'])

        file = open(ARCHLOGO.replace(".png", '.new.svg'), 'w')
        file.write(logo)
        file.close()

        filename_svg = ARCHLOGO.replace(".png", '.new.svg')
        filename_png = ARCHLOGO
        size = 256

        command = "inkscape {filename_svg} -e={filename_png} -C -w={size} -h={size}".format(**locals())
        os.system(command)

        file = open(WALLPAPER.replace(".png", '.svg'), 'r')
        wallpaper = file.read()
        file.close()
        wallpaper = wallpaper.replace("#00ff00", self.theme['panel-top'])
        wallpaper = wallpaper.replace("#ff0000", self.theme['primary'])
        wallpaper = wallpaper.replace("#0000ff", self.theme['primary'])

        #wallpaper = self.set_calendar(wallpaper)

        file = open(WALLPAPER.replace(".png", '.new.svg'), 'w')
        file.write(wallpaper)
        file.close()

        filename_svg = WALLPAPER.replace(".png", '.new.svg')
        filename_png = WALLPAPER
        size_w = 480
        size_h = 320

        # command = "inkscape {filename_svg} -e={filename_png} -C -w={size_w} -h={size_h}".format(**locals())
        command = "convert -resize {size_w}x{size_h} {filename_svg}".format(**locals())

        os.system(command)

    # #----------------------------------------------------------------------
    # def set_calendar(self, wallpaper):
        # """"""
        # month = datetime.date.today().strftime("%B")
        # wallpaper = wallpaper.replace('@month@', month)
        # day = datetime.datetime.now().day
        # w = datetime.date.today().replace(day=1).weekday() + 2

        # if datetime.date.today().month < 12:
        # prev_days_count = (datetime.date.today().replace(day=1, month=datetime.date.today().month) - datetime.timedelta(days=1)).day
        # days_count = (datetime.date.today().replace(day=1, month=datetime.date.today().month+1) - datetime.timedelta(days=1)).day
        # else:
        # days_count = (datetime.date.today().replace(day=1, month=1, year=datetime.date.today().year+1) - datetime.timedelta(days=1)).day

        # #hide days previous month
        # for i in range(1, w):
        # wallpaper = wallpaper.replace('@{}@'.format(str(i).rjust(2, '0')), '{}'.format(prev_days_count-w+i+1))

        # #visible days
        # for i in range(w, days_count+w):
        # wallpaper = wallpaper.replace('@{}@'.format(str(i).rjust(2, '0')), '{}'.format(i-w+1))
        # if day == (i - w + 1):
        # current_day = i
        # #hidden days
        # for i in range(days_count, 43):
        # wallpaper = wallpaper.replace('@{}@'.format(str(i).rjust(2, '0')), '{}'.format(i-days_count-w+1))

        # for i in range(1, 43):
        # b = "#80{}80".format(hex(i)[2:].rjust(2, '0'))

        # if current_day == i:
        # wallpaper = wallpaper.replace(b, self.theme['primary'])
        # else:
        # wallpaper = wallpaper.replace(b, '#000000')

        # return wallpaper

    # ----------------------------------------------------------------------

    @lazy.function
    def to_prev_group(qtile):
        i = qtile.groups.index(qtile.currentGroup)
        qtile.currentScreen.setGroup(qtile.groups[i - 1])

    # ----------------------------------------------------------------------

    @lazy.function
    def to_next_group(qtile):
        i = qtile.groups.index(qtile.currentGroup)
        try:
            qtile.currentScreen.setGroup(qtile.groups[i + 1])
        except:
            qtile.currentScreen.setGroup(qtile.groups[0])

    # ----------------------------------------------------------------------
    # @lazy.function
    # def change_wallpaper(qtile):
        #walpaper = random.choice(os.listdir(WALLPAPER))
        #os.system("feh --bg-center {}".format(os.path.join(WALLPAPER, walpaper)))

    # ----------------------------------------------------------------------

    @lazy.function
    def window_to_prev_group(qtile):
        if qtile.currentWindow is not None:
            i = qtile.groups.index(qtile.currentGroup)
            qtile.currentWindow.togroup(qtile.groups[i - 1].name)
            qtile.currentScreen.setGroup(qtile.groups[i - 1])

    # ----------------------------------------------------------------------

    @lazy.function
    def window_to_next_group(qtile):
        if qtile.currentWindow is not None:
            i = qtile.groups.index(qtile.currentGroup)
            try:
                qtile.currentWindow.togroup(qtile.groups[i + 1].name)
                qtile.currentScreen.setGroup(qtile.groups[i + 1])
            except:
                qtile.currentWindow.togroup(qtile.groups[0].name)
                qtile.currentScreen.setGroup(qtile.groups[0])

    # ----------------------------------------------------------------------

    @lazy.function
    def turn_off_monitor(qtile):
        """"""
        time.sleep(0.5)
        os.system(TURN_OFF_MONITOR)

    # ----------------------------------------------------------------------

    def init_mouse(self):
        """"""
        # Drag floating layouts.
        mouse = [
            Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
            Drag([mod, "shift"], "Button1", lazy.window.set_size_floating(), start=lazy.window.get_size()),
        ]

        return mouse

    # ----------------------------------------------------------------------

    def init_screens(self):
        """"""
        screens = [

            Screen(

                # left=bar.Bar(

                # widgets=[
                # widget.TextBox(text="WTF", background=self.theme["panel-2nd"]),
                # ],

                # size=self.theme["top-height"],
                # background=self.theme["panel-top"],

                # ),


                top=bar.Bar(
                    widgets=[

                        # Logo
                        widget.TextBox(text=" ", background=self.theme["panel-2nd"]),
                        widget.Image(filename=ARCHLOGO, scale=True),

                        # Commands
                        widget.Prompt(fontsize=self.theme["size-md"], cursor_color=self.theme["panel-top"], foreground=self.theme["panel-top"], prompt="$ ", background=self.theme["active"]),
                        #widget.TextBox(text=" ", background=self.theme["active"]),
                        # widget.Sep(foreground=self.theme["separator"]),
                        widget.TextBox(text=" ", background=self.theme["panel-2nd"]),

                        widget.Sep(foreground=self.theme["panel-bottom"], padding=self.theme["separator-padding"] // 2),

                        # widget.AGroupBox(),
                        # widget.Backlight(),

                        # Groups
                        widget.GroupBox(fontsize=self.theme["size-md"], padding=5, borderwidth=self.theme['border-width-active'],
                                        rounded=self.theme["rounded"], this_current_screen_border=self.theme["primary"],
                                        highlight_method=self.theme["group-highlight"], active=self.theme["active"],
                                        inactive=self.theme["inactive"],
                                        highlight_color=self.theme['primary-2nd'],
                                        urgent_text=self.theme['alert'],
                                        urgent_border=self.theme['alert'],
                                        urgent_alert_method=self.theme['group-highlight'],

                                        ),

                        # Spacer
                        widget.Spacer(bar.STRETCH),


                        # Mpris2
                        widget.Mpris2(display_metadata=['xesam:title', 'xesam:album', 'xesam:artist'], fontsize=self.theme["size-md"] * 0.8, objname='org.mpris.MediaPlayer2.spotify', name='Spotify', scroll_chars=128, scroll_interv=0.5, scroll_wait_intervals=8, foreground=self.theme["foreground"]),
                        widget.TextBox(text="   "),


                        # Current Layout
                        # widget.TextBox(text=" ", background=self.theme["panel-2nd"]),
                        # widget.CurrentLayout(background=self.theme["panel-2nd"], foreground=self.theme["foreground-2nd"], fontsize=self.theme["size-md"]*0.8),
                        widget.CurrentLayoutIcon(scale=0.7, background=self.theme["panel-2nd"], foreground=self.theme["foreground-2nd"]),

                    ],

                    size=self.theme["top-height"],
                    background=self.theme["panel-top"],

                ),


                bottom=bar.Bar(
                    widgets=[

                        # Tasklist
                        #widget.TaskList(highlight_method="block", border=self.theme["primary"], fontsize=self.theme["size-lg"], foreground=self.theme["active"], rounded=self.theme["rounded"]),

                        # Window name
                        # widget.WindowName(foreground=self.theme["foreground"]),
                        # widget.CurrentScreen(),


                        # Cmus
                        # widget.Cmus(),

                        # Graphs
                        widget.TextBox(text="net:", fontsize=self.theme["size-xsm"], padding=0, foreground=self.theme["foreground"]),
                        widget.NetGraph(width=40, border_color=self.theme["border-graph"], graph_color=self.theme["graph-color"], fill_color=self.theme["graph-color"], border_width=1, line_width=1, margin_x=0, margin_y=0, samples=50, frequency=1, type="linefill"),

                        widget.TextBox(text=" mem:", fontsize=self.theme["size-xsm"], padding=0, foreground=self.theme["foreground"]),
                        widget.MemoryGraph(width=40, border_color=self.theme["border-graph"], graph_color=self.theme["graph-color"], fill_color=self.theme["graph-color"], border_width=1, line_width=1, margin_x=0, margin_y=0, samples=50, frequency=5, type="linefill"),

                        widget.TextBox(text=" hdd:", fontsize=self.theme["size-xsm"], padding=0, foreground=self.theme["foreground"]),
                        widget.HDDBusyGraph(width=40, border_color=self.theme["border-graph"], graph_color=self.theme["graph-color"], fill_color=self.theme["graph-color"], border_width=1, line_width=1, margin_x=0, margin_y=0, samples=50, frequency=1, type="linefill"),

                        # widget.TextBox(text=" sdd:", fontsize=self.theme["size-xsm"], padding=0, foreground=self.theme["foreground"]),
                        # widget.HDDGraph(border_color=self.theme["border-graph"], graph_color=self.theme["graph-color"], fill_color=self.theme["graph-color"], border_width=1, line_width=1, margin_x=0, margin_y=0, samples=50, frequency=1, type="linefill", space_type='free'),

                        widget.TextBox(text=" cpu:", fontsize=self.theme["size-xsm"], padding=0, foreground=self.theme["foreground"]),
                        widget.CPUGraph(width=40, border_color=self.theme["border-graph"], graph_color=self.theme["graph-color"], fill_color=self.theme["graph-color"], border_width=1, line_width=1, margin_x=0, margin_y=0, samples=50, frequency=1, type="linefill"),

                        # widget.TextBox(text=" swap:", fontsize=self.theme["size-xsm"], padding=0, foreground=self.theme["foreground"]),
                        # widget.SwapGraph(border_color=self.theme["border-graph"], graph_color=self.theme["graph-color"], fill_color=self.theme["graph-color"], border_width=1, line_width=1, margin_x=0, margin_y=0, samples=50, frequency=1, type="linefill"),

                        # #widget.Sep(foreground=self.theme["separator"], border_width=1),


                        # Mem
                        widget.Sep(foreground=self.theme["separator"]),
                        #widget.Sep(foreground=self.theme["panel-bottom"], padding=self.theme["separator-padding"]//2),
                        widget.Memory(foreground=self.theme["foreground"], update_interval=10),

                        # Wifi status
                        # widget.Wlan(interface="wlp2s0"),
                        #widget.Net(interface="wlp2s0", update_interval=10),
                        # widget.Sep(foreground=self.theme["separator"]),

                        # # Thermal
                        # widget.TextBox(text=" ", foreground=self.theme["foreground"]),
                        # #widget.Sep(foreground=self.theme["separator"], padding=self.theme["separator-padding"]),
                        # widget.ThermalSensor(fontsize=self.theme["size-sm"], foreground=self.theme["foreground"], update_interval=1, fmt='{MemUsed}M/{MemTotal}M'),

                        # Debug window
                        # widget.Moc(),
                        # widget.DF(partition='/home'),
                        # widget.DebugInfo(),
                        # widget.Notify(),
                        # widget.Systray(),
                        widget.Sep(foreground=self.theme["separator"], padding=self.theme["separator-padding"]),

                        # # Battery
                        # # widget.BatteryIcon(),
                        # widget.Battery(energy_now_file='charge_now', foreground=self.theme["foreground"]),
                        # widget.Sep(foreground=self.theme["separator"], padding=self.theme["separator-padding"]),

                        # # Volume
                        # widget.TextBox(text="volume:", foreground=self.theme["foreground"]),
                        # widget.Volume(foreground=self.theme["foreground"]),
                        # widget.Sep(foreground=self.theme["separator"], padding=self.theme["separator-padding"]),

                        # Bitcoin
                        #widget.BitcoinTicker(format="BTC: {sell}"),
                        # widget.Sep(foreground=self.theme["separator"]),

                        # # Pacman updates
                        # widget.TextBox(text="pacman:", foreground=self.theme["foreground"]),
                        # widget.Pacman(foreground=self.theme["alert"], unavailable=self.theme["foreground"]),
                        # widget.Sep(foreground=self.theme["panel-bottom"], padding=self.theme["separator-padding"]//2),

                        widget.Spacer(bar.STRETCH),

                        # Clock
                        widget.TextBox(text=" ", background=self.theme["panel-2nd"]),
                        widget.Clock(format="%I:%M:%S %p", foreground=self.theme["foreground-2nd"], background=self.theme["panel-2nd"]),
                        widget.TextBox(text=" ", background=self.theme["panel-2nd"]),

                    ],

                    size=self.theme["bottom-height"],
                    background=self.theme["panel-bottom"],

                ),
            ),
        ]
        return screens

    # ----------------------------------------------------------------------

    def init_widgets(self):
        """"""
        widget_defaults = dict(
            font=self.theme["font-family"],
            fontsize=self.theme["size-sm"],
            padding=3,
        )
        return widget_defaults

    # ----------------------------------------------------------------------

    def init_layouts(self):
        """"""
        layouts = [
            layout.Max(),
            layout.Bsp(border_focus=self.theme["border"], border_normal=self.theme["active"], border_width=self.theme["border-width"]),
            # layout.Columns(),
            # layout.Stack(num_stacks=2, border_focus=self.theme["border"]),
            layout.Matrix(border_focus=self.theme["border"], border_normal=self.theme["active"], border_width=self.theme["border-width"]),
            layout.MonadTall(border_focus=self.theme["border"], border_normal=self.theme["active"], border_width=self.theme["border-width"]),
            layout.MonadWide(border_focus=self.theme["border"], border_normal=self.theme["active"], border_width=self.theme["border-width"]),
            layout.Floating(border_focus=self.theme["border"], border_normal=self.theme["active"], border_width=self.theme["border-width"]),
            #layout.TreeTab(active_bg=self.theme["border"], font=self.theme["font-family"], sections=[""]),
            # layout.Zoomy(columnwidth=300, property_small="0.5", property_big="1.5"),
            layout.RatioTile(border_focus=self.theme["border"], border_normal=self.theme["active"], border_width=self.theme["border-width"], fancy=True),
            # layout.Slice(),
            #layout.Tile(border_focus=self.theme["border"], border_width=self.theme["border-width"]),
            # layout.Wmii(),
        ]
        return layouts

    # ----------------------------------------------------------------------

    def init_floating_layout(self):
        """"""
        # frames = ('Download',
        # 'dropbox',
        # 'file_progress',
        # 'notification',
        # 'toolbar',
        # 'splash',
        # 'dialog',
        # )

        #floating_layout = layout.floating.Floating(float_rules=[{'wmclass': x} for x in frames], border_focus=self.theme["border"], border_normal=self.theme["active"], border_width=self.theme["border-width"])
        floating_layout = layout.floating.Floating(border_focus=self.theme["border"], border_normal=self.theme["active"], border_width=self.theme["border-width"])
        return floating_layout

    # ----------------------------------------------------------------------

    def init_keys(self):
        """"""
        keys = [

            # Qtile commands
            Key([mod, "control"], "r", lazy.restart()),
            Key([mod, "control"], "q", lazy.shutdown()),
            Key([mod, "control"], "t", self.change_theme),

            # Switch between windows in current stack pane
            Key([mod], "k", lazy.layout.down()),
            Key([mod], "j", lazy.layout.up()),

            # Move windows up or down in current stack
            Key([mod, "control"], "k", lazy.layout.shuffle_down()),
            Key([mod, "control"], "j", lazy.layout.shuffle_up()),

            # Resize panels
            Key([mod], "o", lazy.layout.shrink()),
            Key([mod], "p", lazy.layout.grow()),

            # Switch window focus to other pane(s) of stack
            Key([mod], "Right", lazy.layout.next()),
            Key([mod], "Left", lazy.layout.previous()),

            # # Swap panes of split stack
            # Key([mod, "shift"], "space", lazy.layout.rotate()),

            # Toggle between split and unsplit sides of stack.
            # Split = all windows displayed
            # Unsplit = 1 window displayed, like Max layout, but still with
            # multiple stack panes
            # Key([mod, "shift"], "Return", lazy.layout.toggle_split()),

            # Terminal
            Key([mod], "Return", lazy.spawn(TERMINAL)),

            # Toggle between different layouts
            # Key([mod], "space", lazy.nextlayout()),
            Key([mod, "shift"], "Right", lazy.next_layout()),
            Key([mod, "shift"], "Left", lazy.prev_layout()),

            # Close window
            Key([mod, "shift"], "w", lazy.window.kill()),

            # Launch comands
            Key([mod], "r", lazy.spawncmd()),
            Key([mod], "space", lazy.spawncmd()),

            # Maximize window
            Key([mod, "shift"], "Up", lazy.window.toggle_floating()),

            # Full screen
            Key([mod], "f", lazy.window.toggle_fullscreen()),
            Key([mod], "h", self.turn_off_monitor),

            # Multimedia
            Key([], "XF86AudioMute", lazy.spawn(VOLUME_MUTE)),
            Key([], "XF86AudioLowerVolume", lazy.spawn(VOLUME_DOWN)),
            Key([], "XF86AudioRaiseVolume", lazy.spawn(VOLUME_UP)),
            Key([], "XF86MonBrightnessDown", lazy.spawn(BRIGHTNESS_DOWN)),
            Key([], "XF86MonBrightnessUp", lazy.spawn(BRIGHTNESS_UP)),
            Key([], "XF86AudioNext", lazy.spawn(AUDIO_NEXT)),
            Key([], "XF86AudioPrev", lazy.spawn(AUDIO_PREV)),
            Key([], "XF86AudioPlay", lazy.spawn(AUDIO_PLAY)),

            # Move window between groups
            Key([mod, "control", "shift"], "Left", self.window_to_prev_group),
            Key([mod, "control", "shift"], "Right", self.window_to_next_group),

            # Change window focus
            Key([mod, "control"], "Left", self.to_prev_group),
            Key([mod, "control"], "Right", self.to_next_group),

            # Change wallpaper
            #Key([mod], "y", self.change_wallpaper),


            #Key([mod, "shift", "control"], "l", lazy.layout.grow_right()),
            #Key([mod, "shift"], "l", lazy.layout.shuffle_right()),
            #Key([mod, "shift", "control"], "h", lazy.layout.grow_left()),
            #Key([mod, "shift"], "h", lazy.layout.shuffle_left()),
            #Key([mod], "s", lazy.layout.toggle_split()),



        ]

        return keys


coffee = MyQtile()

keys = coffee.keys
groups = coffee.groups
layouts = coffee.layouts
widget_defaults = coffee.widget_defaults
screens = coffee.screens
mouse = coffee.mouse

dgroups_key_binder = None
dgroups_app_rules = []
main = None
follow_mouse_focus = False
bring_front_click = False
cursor_warp = False
auto_fullscreen = True

focus_on_window_activation = 'urgent'

#floating_layout = layout.Floating(border_focus=coffee.theme["border"], border_width=coffee.theme["border-width"])
floating_layout = coffee.floating_layout
# auto_fullscreen = True

# XXX: Gasp! We're lying here. In fact, nobody really uses or cares about this
# string besides java UI toolkits; you can see several discussions on the
# mailing lists, github issues, and other WM documentation that suggest setting
# this string if your java app doesn't work correctly. We may as well just lie
# and say that we're a working one by default.
#
# We choose LG3D to maximize irony: it is a 3D non-reparenting WM written in
# java that happens to be on java's whitelist.
wmname = "LG3D"

# start the applications at Qtile startup
# @hook.subscribe.startup
# def startup():
# ----------------------------------------------------------------------


def main(qtile):
    """"""

    commands = [

        "feh --bg-center {}".format(WALLPAPER),
        #"setxkbmap -layout us -variant intl -option nodeadkeys",
        "setxkbmap -layout us -variant intl",
        "xbacklight -set 100",
        #"xrandr --output LVDS1 --rotate inverted",
    ]

    for command in commands:
        os.system(command)


# @hook.subscribe.client_new
# def floating_dialogs(window):
    #dialog = window.window.get_wm_type() == 'dialog'
    #transient = window.window.get_wm_transient_for()
    # if dialog or transient:
        #window.floating = True

