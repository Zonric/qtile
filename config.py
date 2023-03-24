import os, re, socket, subprocess, colors

from typing import List
from libqtile import hook, qtile, bar, layout, widget
from libqtile.config import Click, Drag, Group, Key, Match, Screen
from libqtile.lazy import lazy
from libqtile.utils import guess_terminal
from libqtile.widget import Spacer, Backlight
from libqtile.widget.image import Image
from libqtile.dgroups import simple_key_binder

###---------------------###
###---	 Variables	 ---###
###---------------------###
mod = "mod4"
terminal = "kitty"
text_editor = terminal + " nvim"
browser = "brave"
file_manager = terminal + " ranger"

###------------------###
###---	 Colors	 ---###
###------------------###
mbfs = colors.mbfs()
doomOne = colors.doomOne()
dracula = colors.dracula()
everforest = colors.everforest()
nord = colors.nord()
gruvbox = colors.gruvbox()

###---	 Color scheme
colorscheme = everforest
colors, backgroundColor, foregroundColor, workspaceColor, foregroundColorTwo = colorscheme

###-----------------------###
###---	 Keybindings	 ---###
###-----------------------###
keys = [
#---------------------------------------------------------------#
#--------------------------Used Key-----------------------------#
#	   A B C D E F G H I J K L M N O P Q R S T U V W X Y Z
#---------------------------------------------------------------#
#    |           x   x x x x x x x x   x x         x       |
#  C |               x   x x x           x                 |
# S  |           x   x   x x x           x                 |
# SC |                                 x                   |
#---------------------------------------------------------------#
#	   A B C D E F G H I J K L M N O P Q R S T U V W X Y Z
#---------------------------------------------------------------#
#	Key([mod], "a", lazy., desc="."),
#	Key([mod], "b", lazy., desc="."),
#	Key([mod], "c", lazy., desc="."),
#	Key([mod], "d", lazy., desc="."),
#	Key([mod], "e", lazy., desc="."),
	Key([mod], "f", lazy.window.toggle_floating(), desc="Toggle window floating."),
#	Key([mod], "g", lazy., desc="."),
	Key([mod], "h", lazy.layout.left(), desc="Move focus to left."),
	Key([mod], "i", lazy.layout.grow(), desc="Increase window space."),
	Key([mod], "j", lazy.layout.down(), desc="Move focus to left."),
	Key([mod], "k", lazy.layout.up(), desc="Move focus to left."),
	Key([mod], "l", lazy.layout.right(), desc="Move focus to left."),
	Key([mod], "m", lazy.layout.shrink(), desc="Decrease window sapce."),
	Key([mod], "n", lazy.layout.normalize(), desc="Reset all window sizes."),
	Key([mod], "o", lazy.layout.decrease_ratio(), desc="Decrease master space."),
#	Key([mod], "p", lazy., desc="."),
	Key([mod], "q", lazy.window.kill(), desc="Kill focused window."),
	Key([mod], "r", lazy.spawn('rofi -show run'), desc="Spawn a command using a prompt widget."),
#	Key([mod], "s", lazy., desc="."),
#	Key([mod], "t", lazy., desc="."),
#	Key([mod], "u", lazy., desc="."),
#	Key([mod], "v", lazy., desc="."),
	Key([mod], "w", lazy.spawn(browser), desc="Launch terminal."),
#	Key([mod], "x", lazy., desc="."),
#	Key([mod], "y", lazy., desc="."),
#	Key([mod], "z", lazy., desc="."),
	Key([mod], "comma", lazy.next_screen(), desc="Switch to monitor left."),
	Key([mod], "period", lazy.prev_screen(), desc="Switch to monitor right."),
	Key([mod], "bracketleft", lazy.screen.prev_group(), desc="Move to group left."),
	Key([mod], "bracketright", lazy.screen.next_group(), desc="Move to group right."),

	Key([mod], "Tab", lazy.layout.next(), desc="Move window focus to other window."),
	Key([mod], "Return", lazy.spawn(terminal), desc="Launch terminal."),
	Key([mod], "Space", lazy.next_layout(), desc="Toggle between layouts."),

	Key([mod, "control"], "h", lazy.layout.grow_left(), desc="Grow window to the left."),
	Key([mod, "control"], "l", lazy.layout.grow_right(), desc="Grow window to the right."),
	Key([mod, "control"], "j", lazy.layout.grow_down(), desc="Grow window down."),
	Key([mod, "control"], "k", lazy.layout.grow_up(), desc="Grow window up."),
	Key([mod, "control"], "r", lazy.reload_config(), desc="Reload the config."),

	Key([mod, "shift"], "f", lazy.window.toggle_fullscreen(), desc="Toggle window fullscreen."),
	Key([mod, "shift"], "h", lazy.layout.shuffle_left(), desc="Move window to the left."),
	Key([mod, "shift"], "l", lazy.layout.shuffle_right(), desc="Move window to the right."),
	Key([mod, "shift"], "j", lazy.layout.shuffle_down(), desc="Move window down."),
	Key([mod, "shift"], "k", lazy.layout.shuffle_up(), desc="Move window up."),
	Key([mod, "shift"], "r", lazy.restart(), desc="Reload Qtile."),
	Key([mod, "shift"], "Return", lazy.layout.toggle_split(), desc="Toggle between split and unsplit sides of stack."),
	Key([mod, "shift"], "comma", lazy.next_screen(), desc="Shift window to monitor left."),
	Key([mod, "shift"], "period", lazy.prev_screen(), desc="Shift window to monitor right."),
	Key([mod, "shift"], "Space", lazy.flip(), desc="Layout flip?."),
	Key([mod, "shift"], "grave", lazy.screen.toggle_group(), desc="Move to the last visied group."),

	Key([mod, "control", "shift"], "q", lazy.shutdown(), desc="Shutdown Qtile."),
]

groups = [Group(i) for i in "123456789"]
for i in groups:
	keys.extend([
		Key(
			[mod],
			i.name,
			lazy.group[i.name].toscreen(),
			desc="Switch to group {}.".format(i.name),
		),
		Key(
			[mod, "shift"],
			i.name,
			lazy.window.togroup(i.name, switch_group=False),
			desc="Move focused window to group {}.".format(i.name),
		),
	])

layouts = [
	layout.MonadTall(ratio=0.75, border_focus=foregroundColor, border_normal=backgroundColor),
	#layout.Columns(),
	layout.Max(),
	#layout.Stack(num_stacks=2),
	#layout.Bsp(),
	#layout.Matrix(),
	#layout.MonadWide(),
	#layout.RatioTile(),
	#layout.Tile(),
	#layout.TreeTab(),
	#layout.VerticalTile(),
	#layout.Zoomy(),
]

widget_defaults = dict(
	font="sans",
	fontsize=12,
	padding=3,
)
extension_defaults = widget_defaults.copy()

screens = [
	Screen(
		top=bar.Bar([
			widget.Image(
				filename="~/.config/qtile/icons/logo.png",
				scale=True,
				margin_x=8,
				mouse_callbacks={'Button1':lambda: qtile.cmd_spawn('rofi -show run')},
			),
			widget.GroupBox(
				padding=5,
				active=colors[2],
				inactive=colors[1],
				highlight_color=[backgroundColor, workspaceColor],
				highlight_method="line",
			),
			widget.WindowName(foreground=colors[5],),
			widget.Volume(
				foreground=colors[4],
				background=foregroundColorTwo,
				fmt=": {}",
				padding=8,
			),
			# widget.Battery(
			# 	charge_char ='',
			# 	discharge_char = '',
			# 	format = '	{percent:2.0%} {char}',
			# 	foreground = colors[6],
			# 	background = foregroundColorTwo,
			# 	padding = 8
			# ),
			widget.Clock(format="%Y-%m-%d %a %I:%M %p",
				foreground=colors[10],
				background=backgroundColor,
				padding=8,
			),
			widget.Systray(),
			widget.QuickExit(
				fmt=" ",
				foreground=colors[9],
				padding=8,
			),
		],24,),
	),
	Screen(
		top=bar.Bar([
			widget.Image(
				filename="~/.config/qtile/icons/logo.png",
				scale=True,
				margin_x=8,
				mouse_callbacks={'Button1':lambda: qtile.cmd_spawn('rofi -show run')},
			),
			widget.GroupBox(
				padding=5,
				active=colors[2],
				inactive=colors[1],
				highlight_color=[backgroundColor, workspaceColor],
				highlight_method="line",
			),
			widget.WindowName(foreground=colors[5],),
			widget.Volume(
				foreground=colors[4],
				background=foregroundColorTwo,
				fmt=": {}",
				padding=8,
			),
			# widget.Battery(
			# 	charge_char ='',
			# 	discharge_char = '',
			# 	format = '	{percent:2.0%} {char}',
			# 	foreground = colors[6],
			# 	background = foregroundColorTwo,
			# 	padding = 8
			# ),
			widget.Clock(format="%Y-%m-%d %a %I:%M %p",
				foreground=colors[10],
				background=backgroundColor,
				padding=8,
			),
			widget.QuickExit(
				fmt=" ",
				foreground=colors[9],
				padding=8,
			),

		],24,),
	),
	Screen(
		top=bar.Bar([
			widget.Image(
				filename="~/.config/qtile/icons/logo.png",
				scale=True,
				margin_x=8,
				mouse_callbacks={'Button1':lambda: qtile.cmd_spawn('rofi -show run')},
			),
			widget.GroupBox(
				padding=5,
				active=colors[2],
				inactive=colors[1],
				highlight_color=[backgroundColor, workspaceColor],
				highlight_method="line",
			),
			widget.WindowName(foreground=colors[5],),
			widget.Volume(
				foreground=colors[4],
				background=foregroundColorTwo,
				fmt=": {}",
				padding=8,
			),
			# widget.Battery(
			# 	charge_char ='',
			# 	discharge_char = '',
			# 	format = '	{percent:2.0%} {char}',
			# 	foreground = colors[6],
			# 	background = foregroundColorTwo,
			# 	padding = 8
			# ),
			widget.Clock(format="%Y-%m-%d %a %I:%M %p",
				foreground=colors[10],
				background=backgroundColor,
				padding=8,
			),
			widget.QuickExit(
				fmt=" ",
				foreground=colors[9],
				padding=8,
			),

		],24,),
	),
]

# Drag floating layouts.
mouse = [
	Drag([mod], "Button1", lazy.window.set_position_floating(), start=lazy.window.get_position()),
	Drag([mod], "Button3", lazy.window.set_size_floating(), start=lazy.window.get_size()),
	Click([mod], "Button2", lazy.window.bring_to_front()),
]

dgroups_key_binder = None
dgroups_app_rules = []	# type: list
follow_mouse_focus = True
bring_front_click = False
cursor_warp = False
floating_layout = layout.Floating(
	float_rules=[
		# Run the utility of `xprop` to see the wm class and name of an X client.
		*layout.Floating.default_float_rules,
		Match(wm_class="confirmreset"),	# gitk
		Match(wm_class="makebranch"),	# gitk
		Match(wm_class="maketag"),	# gitk
		Match(wm_class="ssh-askpass"),	# ssh-askpass
		Match(title="branchdialog"),	# gitk
		Match(title="pinentry"),	# GPG key password entry
	]
)

auto_fullscreen = True
focus_on_window_activation = "smart"
reconfigure_screens = True
auto_minimize = True
wl_input_rules = None
wmname = "LG3D"

