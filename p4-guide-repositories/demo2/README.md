See [README-using-bmv2.md](../README-using-bmv2.md) for some things
that are common across different P4 programs executed using bmv2.

To compile the P4_16 version of the code:

    p4c --target bmv2 --arch v1model demo2.p4_16.p4

To compile the P4_14 version of the code:

    p4c --std p4-14 --target bmv2 --arch v1model demo2.p4_14.p4

The .dot and .png files in the subdirectory 'graphs' were created with
the p4c-graphs program, which is also installed when you build and
install p4c-bm2-ss:

    p4c-graphs -I $HOME/p4c/p4include demo2.p4_16.p4

The '-I' option is only necessary if you did _not_ install the P4
compiler in your system-wide /usr/local/bin directory.

To run the behavioral model with 8 ports numbered 0 through 7:

    sudo simple_switch --log-console --dump-packet-data 10000 -i 0@veth0 -i 1@veth2 -i 2@veth4 -i 3@veth6 -i 4@veth8 -i 5@veth10 -i 6@veth12 -i 7@veth14 demo2.p4_16.json

To run CLI for controlling and examining simple_switch's table
contents:

    simple_switch_CLI

General syntax for table_add commands at simple_switch_CLI prompt:

    RuntimeCmd: help table_add
    Add entry to a match table: table_add <table name> <action name> <match fields> => <action parameters> [priority]

You can find more comprehensive documentation about the `table_add`
and `table_set_default` commands
[here](https://github.com/p4lang/behavioral-model/blob/master/docs/runtime_CLI.md#table_add)
and
[here](https://github.com/p4lang/behavioral-model/blob/master/docs/runtime_CLI.md#table_set_default),
but you do not need to know all of that to understand and use the
example commands here.

----------------------------------------------------------------------
simple_switch_CLI commands for demo2 program
----------------------------------------------------------------------

----------------------------------------------------------------------
demo2.p4_16.p4 only
----------------------------------------------------------------------

The `table_set_default` commands without the `ingressImpl.` and
`egressImpl.` prefixes before `drop_with_count` and `my_drop` used to
work for the P4_16 version of this program, but starting some time
around June 2019 this is no longer the case.

    table_set_default ipv4_da_lpm ingressImpl.drop_with_count
    table_set_default mac_da ingressImpl.my_drop
    table_set_default send_frame egressImpl.my_drop

----------------------------------------------------------------------
demo2.p4_14.p4 only
----------------------------------------------------------------------

    table_set_default ipv4_da_lpm my_drop
    table_set_default mac_da my_drop
    table_set_default send_frame my_drop

----------------------------------------------------------------------
demo2.p4_14.p4 or demo2.p4_16.p4 (same commands work for both)
----------------------------------------------------------------------

Add both sets of entries below:

    table_add ipv4_da_lpm set_l2ptr 10.1.0.1/32 => 58
    table_add mac_da set_bd_dmac_intf 58 => 9 02:13:57:ab:cd:ef 2
    table_add send_frame rewrite_mac 9 => 00:11:22:33:44:55

    table_add ipv4_da_lpm set_l2ptr 10.1.0.200/32 => 81
    table_add mac_da set_bd_dmac_intf 81 => 15 08:de:ad:be:ef:00 4
    table_add send_frame rewrite_mac 15 => ca:fe:ba:be:d0:0d

You should be able to examine counter values in the counter named
ipv4_da_lpm_stats using the `counter_read` command, which takes the
counter name and a handle id.  Because ipv4_da_lpm_stats is declared
`direct` on table ipv4_da_lpm, and thus contains one entry for every
one in ipv4_da_lpm, use the handle id for the corresponding
ipv4_da_lpm table entry that you want stats for.

[ There was a bug with some versions of p4c that prevents counter_read
commands from succeeding, roughly corresponding to p4c source code
from 2017-Nov-07 until 2017-Nov-20.

The "ingressImpl." prefix in the output of some commands below appears
when using the P4_16 version of the program, but not the P4_14
version, due to how p4c names instances based upon the hierarchy of
controls they are instantiated within. ]

    RuntimeCmd: counter_read ipv4_da_lpm_stats 0
    this is the direct counter for table ingressImpl.ipv4_da_lpm
    ipv4_da_lpm_stats[0]=  BmCounterValue(packets=1, bytes=54)

After sending another packet matching the same ipv4_da_lpm entry,
reading the counter entry gives different values:

    RuntimeCmd: counter_read ipv4_da_lpm_stats 0
    this is the direct counter for table ingressImpl.ipv4_da_lpm
    ipv4_da_lpm_stats[0]=  BmCounterValue(packets=2, bytes=108)

The command `counter_reset <name>` clears all counters in the named
collection of counters.

    RuntimeCmd: counter_reset ipv4_da_lpm_stats
    this is the direct counter for table ingressImpl.ipv4_da_lpm

    RuntimeCmd: counter_read ipv4_da_lpm_stats 0
    this is the direct counter for table ingressImpl.ipv4_da_lpm
    ipv4_da_lpm_stats[0]=  BmCounterValue(packets=0, bytes=0)

----------------------------------------------------------------------
scapy session for sending packets
----------------------------------------------------------------------
I believe we must run scapy as root for it to have permission to send
packets on veth interfaces.

```bash
$ sudo scapy
```

```python
fwd_pkt1=Ether() / IP(dst='10.1.0.1') / TCP(sport=5793, dport=80)
drop_pkt1=Ether() / IP(dst='10.1.0.34') / TCP(sport=5793, dport=80)

# Send packet at layer2, specifying interface
sendp(fwd_pkt1, iface="veth0")
sendp(drop_pkt1, iface="veth0")

fwd_pkt2=Ether() / IP(dst='10.1.0.1') / TCP(sport=5793, dport=80) / Raw('The quick brown fox jumped over the lazy dog.')
sendp(fwd_pkt2, iface="veth0")
```

# Last successfully tested with these software versions

For https://github.com/p4lang/p4c

```
$ git log -n 1 | head -n 3
commit fcfb044b0070d78ee3a09bed0e26f3f785598f02
Author: Radostin Stoyanov <rstoyanov@fedoraproject.org>
Date:   Tue Dec 20 16:08:09 2022 +0000
```

For https://github.com/p4lang/behavioral-model

```
$ git log -n 1 | head -n 3
commit e97b6a8b4aec6da9f148326f7677f5e46b09e5ee
Author: Radostin Stoyanov <rstoyanov@fedoraproject.org>
Date:   Mon Dec 12 21:05:06 2022 +0000
```
