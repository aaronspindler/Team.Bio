# Team.Bio

[![Test and Deploy](https://github.com/aaronspindler/Team.Bio/actions/workflows/test-and-deploy.yml/badge.svg)](https://github.com/aaronspindler/Team.Bio/actions/workflows/test-and-deploy.yml)
[![CodeCov](https://codecov.io/gh/aaronspindler/Team.Bio/branch/main/graph/badge.svg?token=V0KWJT21BP)](https://codecov.io/gh/aaronspindler/Team.Bio)

### Local Setup

1. Create virtual env
2. Install requirements `pip install -r requirements.txt`
3. Hook in pre-commit `pre-commit install`
4. Copy .env.example to .env and fill in the values
5. Run `python manage.py migrate`
6. Run `python manage.py createsuperuser`

### Icons

Get icons from [iconoir](https://iconoir.com), make sure to create a normal (black) and light (white) version
Size 24
Stroke Width 1.5

### Environment Variables

If you add a new environment variable to settings, you will also need to add the variable to https://github.com/aaronspindler/Team.Bio/blob/main/.github/workflows/test-and-deploy.yml in the env section

### Useful Commands

`stripe listen --forward-to localhost:8000/billing/webhook` generates a local webhook listener so that you can test stripe webhook