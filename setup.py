import __modules__.cli as cli
import __modules__.env as env
import __modules__.fileutil as fu
import __modules__.misc as misc

fu.admin()

modules = fu.join(fu.PYDIR, "__modules__")
env.add("PYTHONPATH", modules, stdout=False)

packages = [
    "Pillow",
    "NumPy",
    "Pyglet",
    "OpenSimplex"
]

for pkg in packages:
    cli.heading(pkg)
    misc.install(pkg)

cli.line()

cli.enter("exit")
