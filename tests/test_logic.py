
import conftest

import shader_link.app

def _disable_export (config):
    config.temp_export_path = None
    config.target_export_path = None

def _disable_forced (config):
    config.forced = False

def _run_app (config, compiler):
    app = shader_link.app.App(config)
    app.run ()

def test_success (config, good_compiler, input_files, tracker):
    _disable_export (config)
    _disable_forced (config)

    _run_app (config, good_compiler)

    tracker.successful_compilation.assert_called ()
    tracker.failed_compilation.assert_not_called ()

def test_fail (config, bad_compiler, input_files, tracker):
    _disable_export (config)
    _disable_forced (config)

    _run_app (config, bad_compiler)

    tracker.successful_compilation.assert_not_called ()
    tracker.failed_compilation.assert_called ()

def test_skip (config, good_compiler, input_files, tracker):
    _disable_export (config)
    _disable_forced (config)

    _run_app (config, good_compiler)

    tracker.successful_compilation.assert_called ()
    tracker.failed_compilation.assert_not_called ()
    tracker.skip.assert_not_called ()

    tracker.reset_mock ()
    _run_app (config, good_compiler)

    tracker.skip.assert_called ()

def test_forced (config, good_compiler, input_files, tracker):
    _disable_export (config)
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
