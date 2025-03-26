import pytest
from main import handle_echo, handle_pwd, handle_cd, handle_type, handle_exit
from unittest.mock import patch

# Test File #

def test_handle_echo(capsys):
    """testing handle_echo method"""
    handle_echo(["Hello", "World"])
    captured = capsys.readouterr()
    assert captured.out == "Hello World\n"
    
    handle_echo([])
    captured = capsys.readouterr()
    assert captured.out == "\n"
    
    handle_echo(["@#$%^   ", "iioo"])
    captured = capsys.readouterr()
    assert captured.out == "@#$%^    iioo\n"


def test_handle_pwd(capsys):
    """testing handle_pwd method"""
    with patch("pathlib.Path.cwd") as mock_pwd:
        mock_pwd.return_value = "/fake/home/directory"
        handle_pwd()
        captured = capsys.readouterr()
        assert captured.out == "/fake/home/directory\n"

def test_handle_cd():
    """testing handle_cd method"""
    with patch("os.chdir") as mock_dir:
        handle_cd('/dd/oo')
        mock_dir.assert_called_with('/dd/oo')

    with patch("os.chdir") as mock_dir: 
        handle_cd("~")
        mock_dir.assert_called_with('/home/parsa')

def test_handle_exit():
    """testing handle_exit method"""
    with pytest.raises(SystemExit): 
            handle_exit()
        
def test_type_builtin(capsys):
    """testing builting detection in handle_type"""
    handle_type("echo")
    captured = capsys.readouterr()
    assert captured.out == "echo is a shell builtin\n"

@patch('shutil.which', return_value="/usr/local/bin/python")
def test_type_custom_path(mock_which, capsys):
    """testing external detection in handle_type"""
    handle_type("python")
    captured = capsys.readouterr()
    assert captured.out == "python is /usr/local/bin/python\n"