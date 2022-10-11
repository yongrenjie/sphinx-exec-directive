import pytest

# see https://github.com/sphinx-doc/sphinx/issues/7008

def test(app, shared_result):
    # app is a Sphinx application object for default sphinx project (`tests/roots/test-root`).
    written = []
    app.builder._warn_out = written.append
    app.build()
    print(written)

# @pytest.mark.sphinx(buildername='latex')
# def test_latex(app):
#      # latex builder is chosen here.
#      app.build()

# @pytest.mark.sphinx(testroot='case1')
# def test_case1(app):
#     # app is Sphinx application for case1 sphinx project (`tests/roots/test-case1`)
#     app.build()

# @pytest.mark.sphinx(confoverrides={'master_doc': 'content'})
# def test_confoverrides(app):
#     # a Sphinx application configured with given setting
#     app.build()
