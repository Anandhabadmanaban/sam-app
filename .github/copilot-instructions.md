# Copilot Instructions for sam-app

## Project Overview
This is a serverless AWS SAM application using Python 3.9, DynamoDB, Lambda, and API Gateway. The architecture is defined in `template.yaml` and code is organized under `src/` and root-level files. The project is designed for deployment and local emulation using the SAM CLI.

## Key Files & Structure
- `app.py` (root): Main Lambda handler
- `src/app.py`: Additional application logic (check usage)
- `template.yaml`: AWS resources, API Gateway routes, Lambda definitions
- `events/`: Sample event payloads for local invocation
- `tests/`: Contains `unit/` and `integration/` test suites
- `requirements.txt`: Python dependencies for Lambda
- `tests/requirements.txt`: Test dependencies

## Developer Workflows
### Build & Deploy
- Build: `sam build` or `sam build --use-container`
- Deploy: `sam deploy --guided` (prompts for stack name, region, IAM, etc.)
- Local API emulation: `sam local start-api` (serves on port 3000)
- Delete stack: `sam delete --stack-name "sam-app"`

### Testing
- Install test deps: `pip install -r tests/requirements.txt --user`
- Run unit tests: `python -m pytest tests/unit -v`
- Run integration tests (after deploy):
  - Set env: `AWS_SAM_STACK_NAME="sam-app"`
  - Run: `python -m pytest tests/integration -v`

### Debugging & Logs
- Fetch Lambda logs: `sam logs -n <FunctionName> --stack-name "sam-app" --tail`
- Use `sam logs` for troubleshooting deployed functions

## Patterns & Conventions
- API Gateway routes and Lambda event bindings are defined in `template.yaml` under the `Events` property
- Use `events/event.json` for local invocation payloads
- All AWS resources are managed via SAM/CloudFormation; update `template.yaml` for changes
- Test code is separated into `unit/` and `integration/` folders; integration tests require a deployed stack

## External Dependencies
- AWS SAM CLI, Docker, Python 3.9
- AWS account with permissions for Lambda, API Gateway, DynamoDB

## Examples
- To add a new API route, update the `Events` section in `template.yaml` and implement the handler in `app.py`
- To run the API locally: `sam local start-api` then `curl http://localhost:3000/`
- To run all tests: `pip install -r tests/requirements.txt --user` then `pytest tests/`

## References
- See `README.md` for more details and links to AWS documentation
- For resource types, refer to [SAM specification](https://github.com/awslabs/serverless-application-model/blob/master/versions/2016-10-31.md)

---
_If any workflow, convention, or integration is unclear, ask the user for clarification or examples from their usage._
