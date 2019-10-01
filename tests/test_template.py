import pytest


@pytest.fixture
def base_context():
    """Test template creation with test parameters."""
    return {
        "full_name": "test name",
        "email": "test@email.com",
        "github_username": "test_username",
        "repo_name": "test_repo",
        "package_name": "test_repo",
        "project_short_description": "Test description.",
        "version": "0.1.0",
    }


def test_template(cookies, base_context):
    """Test the template for proper creation.

    cookies is a fixture provided by the pytest-cookies
    plugin. Its bake() method creates a temporary directory
    and installs the cookiecutter template into that directory.
    """
    result = cookies.bake(extra_context=base_context)

    assert result.exit_code == 0
    assert result.exception is None
    assert result.project.basename == 'test_repo'
    assert result.project.isdir()


def test_has_license(cookies):
    context = {
        "full_name": "test name",
        "email": "test@email.com",
        "github_username": "test_username",
        "repo_name": "test_repo",
        "package_name": "test_repo",
        "project_short_description": "Test description.",
        "version": "0.1.0",
        "open_source_license": "BSD"
    }
    result = cookies.bake(extra_context=context)
    assert result.exit_code == 0
    assert result.exception is None
    assert result.project.join('LICENSE').check(file=1)


def test_no_license(cookies):
    context = {
        "full_name": "test name",
        "email": "test@email.com",
        "github_username": "test_username",
        "repo_name": "test_repo",
        "package_name": "test_repo",
        "project_short_description": "Test description.",
        "version": "0.1.0",
        "open_source_license": "Proprietary"
    }
    result = cookies.bake(extra_context=context)
    assert result.exit_code == 0
    assert result.exception is None
    assert not result.project.join('LICENSE').check(file=1)

def test_noararch(cookies):
    context = {
        "full_name": "test name",
        "email": "test@email.com",
        "github_username": "test_username",
        "repo_name": "test_repo",
        "package_name": "test_repo",
        "project_short_description": "Test description.",
        "version": "0.1.0",
        "open_source_license": "Proprietary",
        "noarch_python": "True"
    }
    result = cookies.bake(extra_context=context)
    assert result.exit_code == 0
    assert result.exception is None
    with result.project.join('conda.recipe','meta.yaml').open() as f:
        recipe = f.read()
        assert "noarch: python" in recipe

    context['noarch_python'] = 'False'
    result = cookies.bake(extra_context=context)
    assert result.exit_code == 0
    assert result.exception is None
    with result.project.join('conda.recipe','meta.yaml').open() as f:
        recipe = f.read()
        assert "noarch: python" not in recipe

