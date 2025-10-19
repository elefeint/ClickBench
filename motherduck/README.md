## Prerequisite

* Get a [MotherDuck token](https://motherduck.com/docs/key-tasks/authenticating-and-connecting-to-motherduck/authenticating-to-motherduck/#creating-an-access-token)


## Running the benchmark

Pass `motherduck_instance_type=<INSTANCE_TYPE>` to determine the report name and description.
By default, the report will be named `log.json` and the instance type will be reported as "unknown instance type"

By default, running `benchmark.sh` will try to install python.
To skip that step:
```
 bash benchmark.sh --skip-setup
```