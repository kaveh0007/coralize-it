# Problem Statement 
During a high-pressure incident, engineers lose critical minutes jumping between browser tabs. Information is siloed:
- Sentry knows what broke.
- GitHub knows who changed the code.

**coralize-it** aims to solve it by using the capabilities provided by [**coral**](https://github.com/withcoral/coral) (which provides a SQL runtime over various datasources including github and sentry) and reduce the `mean time to resolution (MTTR)` during system outages.