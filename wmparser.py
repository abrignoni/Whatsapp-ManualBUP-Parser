import sys, os, re
import glob
import io
import sys
import pathlib
import datetime

import PySimpleGUI as sg

sg.theme('LightGreen3')   # Add a touch of color
# All the stuff inside your window.

layout = [  [sg.Text('SCSO - Whatsapp Manual Extraction Report Generator.', font=("Helvetica", 25))], #added font type and font size
			[sg.Text('Select directory containing the extracted files per folder.', font=("Helvetica", 16))],#added font type and font size
			[sg.Text('Directory:', size=(8, 1), font=("Helvetica", 14)), sg.Input(), sg.FolderBrowse(font=("Helvetica", 12))], #added font type and font size
			[sg.Output(size=(100,40))], #changed size from (88,20)
			[sg.Submit('Process',font=("Helvetica", 14)), sg.Button('Close', font=("Helvetica", 14))] ] #added font type and font size
			

# Create the Window
window = sg.Window('SCSO', layout)
# Event Loop to process "events" and get the "values" of the inputs
while True:
	event, values = window.read()
	if event in (None, 'Close'):   # if user closes window or clicks cancel
		break
	
	pathto = values[0]
	if os.path.isdir(pathto):
		pass
	else:
		sg.PopupError('No path or the one selected is invalid. Run the program again.', pathto)
		sys.exit()


	count = 0
	now = datetime.datetime.now()
	currenttime = str(now.strftime('%Y-%m-%d_%A_%H%M%S'))
	reportfolder = './_Whatsapp_Report_'+currenttime+'/'
	#chatsdir = '/Users/abrignoni/Desktop/WhatsappScript/WhatsAppData'
	os.makedirs(reportfolder)

	chatsdir = pathlib.Path(pathto)
	datafolder = chatsdir.parts[-1]
	print (f'Processing started.')
	print (f'Selected directory: {chatsdir}')
	print ('')
	#create main report folder usando timestamp
	for root, dirs, files in sorted(os.walk(chatsdir)):
		for file in files:
			if file.endswith(".txt"):	
				fullpath = (os.path.join(root, file))
				head, tail = os.path.split(fullpath)
				p = pathlib.Path(fullpath)
				#print (fullpath)
				folder = (p.parts[-2])
				count = count + 1
				#create folder for the chat usando la variable folder para nombrarlo
				with open(reportfolder+'/Chat '+str(count)+'-'+folder+'.html','w') as r:
					with open(fullpath) as f:
						#print(tail)
						#print(folder)
						#print('')
						r.write('<html><body>')
						r.write('<head><style>tr:nth-child(even) {background-color: #f2f2f2;}</style>')
						r.write('<table>')
						r.write('<tr><td><img src="../logo.jpg" alt="logo" style="width:200px;height:200px;"><td <strong style="font-size: 35px;">Whatsapp Chat Content Report</strong></td></tr>')
						r.write('</table>')
						r.write('<br>')
						r.write('<table border = "1px solid black" style="border-collapse: collapse;">')
						for line in f:
							#print(line)
							r.write(f'<tr><td>{line}</td>')
							mediaObj = re.search( r"(file attached)", line)
							if mediaObj:
								mediaclean = re.search(r"((?<=: )(.*)(?= \(file attached))", line)
								if mediaclean:
									media = (mediaclean.group(1))
									r.write(f'<td><a href = "../{datafolder}/{folder}/{media}">{media}</a></td></tr>')
							else:
								r.write(f'<td> </td></tr>')	
						r.write('</table></body></html>')
						print(f'Processing chat #{str(count)}')
	print('')
	if count == 0:
		print(f'No chats found/processed.')
	else:
		print(f'Total chats processed: {str(count)}')