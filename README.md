<div align="center">
  
  <img src="https://res.cloudinary.com/ix-48/image/upload/v1594108320/logo-wide-light.svg" />

  <br/>
  <div style="color: #808080; font-style:italic;">
    <h3>
      ROUTING POLICY
    </h3>
  </div>

</div>

<hr/>

This repository contains code used for automatically generating routing policy for [48 IX](https://48ix.net).

## How it Works

The Route Policy Server (RPS) performs the following for each [48 IX participant](https://48ix.net/participants):

- Generates IPv4 & IPv6 prefix-lists based on [NTT's IRR database](https://www.gin.ntt.net/support-center/policies-procedures/routing-registry/)
- Generates per-participant BGP standard, extended, and large community lists
- Generates per-participant route-maps to implement the [48 IX Routing Policy](https://48ix.net/connection-policy)
- Generates per-participant BGP configs
  - Pulls the `info_prefixes4` and `info_prefixes6` attributes via the [PeeringDB](https://peeringdb.com) REST API, and uses them as the `maximum-prefix` value for the corresponding participant (if none is set, values of 200 and 20 are set for IPv4 & IPv6, respectively)
- Combines policies for all peers, sends the net policy to [48 IX Route Servers](https://48ix.net/network) via [Route Server Agent](https://github.com/48ix/rsagent) (RSA)

## Contributing

48 IX Participants may feel free to submit pull requests under the following circumstances:

- A verified bug is being fixed
- A feature is being added which maintains the 48 IX Connection Agreement and benefits all participants
- Performance is improved

If you would like to contribute, please [email the NOC](mailto:noc@48ix.net) to discuss code quality standards and development processes.
