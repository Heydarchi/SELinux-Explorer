from PolicyEntities import *


###############################################################################################

#https://source.android.com/docs/security/features/selinux/implement#context-files
#https://github.com/SELinuxProject/selinux-notebook/blob/main/src/seandroid.md#file_contexts
#https://android.googlesource.com/platform/system/sepolicy/

#Context files

policyFiles = list()
policyFiles.append( PolicyFiles('file_contexts','assigns labels to files and is used by various userspace components'))





###############################################################################################

#https://source.android.com/docs/security/features/selinux/customize

#Available controls

controls = list()
controls.append(Controls('file', {'ioctl','read','write','create','getattr','setattr','lock','relabelfrom','relabelto','append',
'unlink','link','rename','execute','swapon','quotaon','mounton'}))