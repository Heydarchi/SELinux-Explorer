
neverallow artd ~{art_exec_exec}:file execute_no_trans;

neverallow * ~{ system_file_type vendor_file_type rootfs }:system module_load;

neverallow { domain -init -vendor_init -dumpstate } debugfs:{ file lnk_file } no_rw_file_perms;

allow usbhubfwupgrade_$1 usbhubfwupgrade:fd { use };

