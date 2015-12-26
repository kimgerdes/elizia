#!/usr/bin/python
# -*- coding: utf-8 -*-

####
# Copyright (C) 2014 Kim Gerdes
# kim AT gerdes.fr
#
# This program is free software; you can redistribute it and/or
 # modify it under the terms of the GNU General Public License
 # as published by the Free Software Foundation; either version 2
 # of the License, or (at your option) any later version.
#
# This script is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE
# See the GNU General Public License (www.gnu.org) for more details.
#
# You can retrieve a copy of the GNU General Public License
# from http://www.gnu.org/.  For a copy via US Mail, write to the
#     Free Software Foundation, Inc.
#     59 Temple Place - Suite 330,
#     Boston, MA  02111-1307
#     USA
####

import subprocess

args=["./buildlexicon -d . -p lemmdico consult"]

def lookup(query):
	query="\n".join(query.split())+"\n"
	p = subprocess.Popen(args ,stdout=subprocess.PIPE, shell=True,stdin=subprocess.PIPE, stderr=subprocess.PIPE)
	(stdoutdata, stderrdata) = p.communicate(query)
	#print (stdoutdata, stderrdata)
	return stdoutdata.split()

if __name__ == "__main__":
	print lookup("qsdf aimerions qsdf qsdf nous viens")
