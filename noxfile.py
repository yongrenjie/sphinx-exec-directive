import nox

nox.options.sessions = ["test"]


@nox.session
def black(session):
    session.install("black")
    session.run("black", ".")


@nox.session
@nox.parametrize(
    "sphinx_version", ["4.4.0", "4.5.0", "5.0.2", "5.1.1", "5.2.3", "5.3.0"]
)
def test(session, sphinx_version):
    session.install("pytest")
    session.install("sphinx=={}".format(sphinx_version))
    session.run("pytest")
