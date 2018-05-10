def test_development_config(app):
    app.config.from_object('config.DevConfig')
    assert app.config['DEBUG']
    assert not app.config['TESTING']
