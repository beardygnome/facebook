#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#  untitled.py
#
#  Copyright 2012 Phil Whitaker <phil<at>philipwhitaker<dot>co<dot>uk>
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.

import sys
import os

class Config:
	person = "Unknown"
	output_error = False


def get_dir_name(path):
	'''
	(str) -> str

	Returns the final element of path, with any trailing '/' removed.

	>>> get_dir_name('/home/philip/Projects/')
	'Projects'
	>>> get_dir_name('/media/usb')
	'usb'
	'''
	if path.endswith("/"):
		dir = path[:-1]
	else:
		dir = path

	dir_root, dir_name = os.path.split(dir)

	return dir_name


def main():
	num_args = len(sys.argv)

	if num_args < 3 or num_args > 4:
		show_usage()
		return 2
	else:
		Config.output_error = sys.argv[1]

		if not Config.output_error.isnumeric():
			show_usage()
			return 2
		else:
			Config.output_error = bool(int(Config.output_error))

		dir = sys.argv[2]

		if not os.path.isdir(dir):
			print(dir, " is not a directory!")
			return 3

		if num_args == 4:
			out = open(sys.argv[4], "w")
		else:
			dir_name = get_dir_name(dir)
			file_name = dir_name + ".html"
			out = open(file_name, "w")

		out.write("<?xml version='1.0' encoding='utf-8'?>\n<html>\n")

		out.write(process_dir(dir))

		out.write("</html>")
		out.close()


	return 0


def process_dir(dir):
	text = ""

	for root, dirs, files in os.walk(dir):
		person = get_dir_name(root);
		text += "\t<br/>\n\t<br/>\n\t<strong>{0}:</strong>\n\t<br/>\n"
		text = text.format(person)

		for file in files:
			if os.path.splitext(file)[1] == ".jpg":
				file_path = os.path.join(root, file)
				text += "\t\t{0}\n".format(process_file(file_path, person))

	return text


def process_file(file, person):
	PHOTO_URL = "https://www.facebook.com/photo.php?"
	PROFILE_URL = "https://www.facebook.com/profile.php?"
	ignore = False
	text = ""

	root, filename = os.path.split(file)
	filename, ext = os.path.splitext(filename)

	if filename.startswith("n"):
		photo_args, profile_args = process_file_first_gen(filename, person)
		photo_url = PHOTO_URL + photo_args
		profile_url = PROFILE_URL + profile_args
	elif filename.endswith("n"):
		count = filename.count("_")

		if count == 5:
			photo_args, profile_args = process_file_second_gen(filename, person)
			photo_url = PHOTO_URL + photo_args
			profile_url = PROFILE_URL + profile_args
		elif count == 3:
			photo_args = process_file_third_gen(filename, person)
			photo_url = PHOTO_URL + photo_args
			profile_url = ""
		else:
			pass#raise InvalidUrlError
	elif filename.endswith("a"):
		ignore = True
	else:
		photo_url = "Error: " + filename
		profile_url = ""
		pass

	#FIX THIS LOGIC - IT DOESN'T WORK PROPERLY!!!!
	if not ignore and not (Config.output_error):# or not error):
		text += "\t<table style='display: inline'>\n\t\t<tr>\n\t\t\t<td>\n"
		text += "\t\t\t\t<a href='" + photo_url + "'>\n\t\t\t\t\t<img src='"
		text +=	file + "' alt='" + person +	"' title='" + person
		text +=	"' style='height: 30%'/>\n\t\t\t\t</a>\n\t\t\t</td>\n\t\t</tr>\n"

		if (profile_url):
			text += "\t\t<tr>\n\t\t\t<td>\n\t\t\t\t<a href='"
			text += profile_url + "'>\n\t\t\t\t\tProfile\n\t\t\t\t</a>\n"
			text += "\t\t\t</td>\n\t\t</tr>\n"

		text += "\t</table>\n"

	return text


def process_file_first_gen(filename, person):
	try:
		first_ = filename.index("_")
		second_ = filename.index("_", first_ + 1)
	except ValueError as ex:
		pass#raise InvalidUrlError
	else:
		id_start = 1
		id_end = first_
		id = filename[id_start:id_end]

		if "n" in id:
			pass#raise InvalidIdError

		pid_start = first_ + 1
		pid_len = second_ - pid_start
		pid = filename[pid_start:pid_start + pid_len]

		if "n" in pid:
			pass#raise InvalidPidError

	photo_url_args = "pid=" + pid + "&id=" + id
	profile_url_args = "id=" + id

	return photo_url_args, profile_url_args


def process_file_second_gen(filename, person):
	try:
		first_ = filename.index("_")
		second_ = filename.index("_", first_ + 1)
		third_ = filename.index("_", second_ + 1)
	except ValueError as ex:
		pass
	else:
		id_start = second_ + 1
		id_len = third_ - id_start
		id = filename[id_start:id_start + id_len]

		if "n" in id:
			pass#raise InvalidIdError

	try:
		fourth_ = filename.index("_", third_ + 1)
		#fifth_ = filename.index("_", fourth_ + 1)
	except ValueError as ex:
		pass
	else:
		pid_start = third_ + 1
		pid_len= fourth_ - pid_start
		pid = filename[pid_start:pid_start + pid_len]

		if "n" in pid:
			pass#raise InvalidPidError

	photo_url_args = "pid=" + pid + "&id=" + id
	profile_url_args = "id=" + id

	return photo_url_args, profile_url_args


def process_file_third_gen(filename, person):
	try:
		first_ = filename.index("_")
		second_ = filename.index("_", first_ + 1)
		#third_ = filename.index("_", second_ + 1)
	except ValueError as ex:
		pass
	else:
		fbid_start = first_ + 1
		fbid_len = second_ - fbid_start
		fbid = filename[fbid_start:fbid_start + fbid_len]

		if "n" in fbid:
			pass#raise InvalidFbidError

	photo_url_args = "fbid=" + fbid

	return photo_url_args


if __name__ == '__main__':
	#main()
	import doctest
	doctest.testmod()
