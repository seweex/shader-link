
import conftest

import shader_link.app

def _run_app (config, compiler):
    app = shader_link.app.App(config)
    app.run ()

def test_success (config, good_compiler, input_files, tracker):
    config.export_path = None
    config.forced = False

    _run_app (config, good_compiler)

    tracker.successful_compilation.assert_called ()
    tracker.failed_compilation.assert_not_called ()

def test_fail (config, bad_compiler, input_files, tracker):
    config.export_path = None
    config.forced = False

    _run_app (config, bad_compiler)

    tracker.successful_compilation.assert_not_called ()
    tracker.failed_compilation.assert_called ()

def test_skip (config, good_compiler, input_files, tracker):
    config.export_path = None
    config.forced = False

    _run_app (config, good_compiler)

    tracker.successful_compilation.assert_called ()
    tracker.failed_compilation.assert_not_called ()
    tracker.skip.assert_not_called ()

    tracker.reset_mock ()
    _run_app (config, good_compiler)

    tracker.skip.assert_called ()

def test_forced (config, good_compiler, input_files, tracker):
    config.export_path = None
    config.forced = True
    _run_app(config, good_compiler)

    tracker.successful_compilation.assert_called()
    tracker.failed_compilation.assert_not_called()
    tracker.skip.assert_not_called()

    tracker.reset_mock ()
    _run_app(config, good_compiler)

    tracker.successful_compilation.assert_called()
    tracker.failed_compilation.assert_not_called()
    tracker.skip.assert_not_called()

def test_export (config, good_compiler, input_files, tracker):
    _run_app(config, good_compiler)

    tracker.successful_compilation.assert_called()
    tracker.successful_export.assert_called()
    tracker.failed_compilation.assert_not_called()
    tracker.failed_export.assert_not_called()
