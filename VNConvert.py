# -*- coding: utf-8 -*-
# Simple script for conversion of Vietnamese encoding
# ---------------------------------------------------
# Modified by Chu Quang Thao - chuquangthao@gmail.com - in 2014
# Reference:
# - Ninomax - thanhlv@oucru.org - 19/01/2010 # Mapping team - The Oxford University Clinical Research Unit, Ha Noi
# - Quách Đồng Thắng (vnosgis.blogspot.com), Trung tâm Ứng dụng GIS Tp.HCM (hcmgisportal.vn). 

import arcpy, os
arcpy.env.overwriteOutput = 1

# Array of characters
global _Unicode, _TCVN3, _VNIWin, _KhongDau
# global _upper, _lower, _capitalize, _title, _none
_Unicode = [
    u'â',u'Â',u'ă',u'Ă',u'đ',u'Đ',u'ê',u'Ê',u'ô',u'Ô',u'ơ',u'Ơ',u'ư',u'Ư',u'á',u'Á',u'à',u'À',u'ả',u'Ả',u'ã',u'Ã',u'ạ',u'Ạ',
    u'ấ',u'Ấ',u'ầ',u'Ầ',u'ẩ',u'Ẩ',u'ẫ',u'Ẫ',u'ậ',u'Ậ',u'ắ',u'Ắ',u'ằ',u'Ằ',u'ẳ',u'Ẳ',u'ẵ',u'Ẵ',u'ặ',u'Ặ',
    u'é',u'É',u'è',u'È',u'ẻ',u'Ẻ',u'ẽ',u'Ẽ',u'ẹ',u'Ẹ',u'ế',u'Ế',u'ề',u'Ề',u'ể',u'Ể',u'ễ',u'Ễ',u'ệ',u'Ệ',u'í',u'Í',u'ì',u'Ì',u'ỉ',u'Ỉ',u'ĩ',u'Ĩ',u'ị',u'Ị',    
    u'ó',u'Ó',u'ò',u'Ò',u'ỏ',u'Ỏ',u'õ',u'Õ',u'ọ',u'Ọ',u'ố',u'Ố',u'ồ',u'Ồ',u'ổ',u'Ổ',u'ỗ',u'Ỗ',u'ộ',u'Ộ',u'ớ',u'Ớ',u'ờ',u'Ờ',u'ở',u'Ở',u'ỡ',u'Ỡ',u'ợ',u'Ợ',    
    u'ú',u'Ú',u'ù',u'Ù',u'ủ',u'Ủ',u'ũ',u'Ũ',u'ụ',u'Ụ',u'ứ',u'Ứ',u'ừ',u'Ừ',u'ử',u'Ử',u'ữ',u'Ữ',u'ự',u'Ự',u'ỳ',u'Ỳ',u'ỷ',u'Ỷ',u'ỹ',u'Ỹ',u'ỵ',u'Ỵ',u'ý',u'Ý'    
]
_TCVN3 = [
    u'©',u'¢',u'¨',u'¡',u'®',u'§',u'ª',u'£',u'«',u'¤',u'¬',u'¥',u'­',u'¦',u'¸',u'¸',u'µ',u'µ',u'¶',u'¶',u'·',u'·',u'¹',u'¹',
    u'Ê',u'Ê',u'Ç',u'Ç',u'È',u'È',u'É',u'É',u'Ë',u'Ë',u'¾',u'¾',u'»',u'»',u'¼',u'¼',u'½',u'½',u'Æ',u'Æ',
    u'Ð',u'Ð',u'Ì',u'Ì',u'Î',u'Î',u'Ï',u'Ï',u'Ñ',u'Ñ',u'Õ',u'Õ',u'Ò',u'Ò',u'Ó',u'Ó',u'Ô',u'Ô',u'Ö',u'Ö',u'Ý',u'Ý',u'×',u'×',u'Ø',u'Ø',u'Ü',u'Ü',u'Þ',u'Þ',    
    u'ã',u'ã',u'ß',u'ß',u'á',u'á',u'â',u'â',u'ä',u'ä',u'è',u'è',u'å',u'å',u'æ',u'æ',u'ç',u'ç',u'é',u'é',u'í',u'í',u'ê',u'ê',u'ë',u'ë',u'ì',u'ì',u'î',u'î',    
    u'ó',u'ó',u'ï',u'ï',u'ñ',u'ñ',u'ò',u'ò',u'ô',u'ô',u'ø',u'ø',u'õ',u'õ',u'ö',u'ö',u'÷',u'÷',u'ù',u'ù',u'ú',u'ú',u'û',u'û',u'ü',u'ü',u'þ',u'þ',u'ý',u'ý'     
]
_VNIWin = [
    u'aâ',u'AÂ',u'aê',u'AÊ',u'ñ',u'Ñ',u'eâ',u'EÂ',u'oâ',u'OÂ',u'ô',u'Ô',u'ö',u'Ö',u'aù',u'AÙ',u'aø',u'AØ',u'aû',u'AÛ',u'aõ',u'AÕ',u'aï',u'AÏ',
    u'aá',u'AÁ',u'aà',u'AÀ',u'aå',u'AÅ',u'aã',u'AÃ',u'aä',u'AÄ',u'aé',u'AÉ',u'aè',u'AÈ',u'aú',u'AÚ',u'aü',u'AÜ',u'aë',u'AË',
    u'eù',u'EÙ',u'eø',u'EØ',u'eû',u'EÛ',u'eõ',u'EÕ',u'eï',u'EÏ',u'eá',u'EÁ',u'eà',u'EÀ',u'eå',u'EÅ',u'eã',u'EÃ',u'eä',u'EÄ',u'í',u'Í',u'ì',u'Ì',u'æ',u'Æ',u'ó',u'Ó',u'ò',u'Ò',    
    u'où',u'OÙ',u'oø',u'OØ',u'oû',u'OÛ',u'oõ',u'OÕ',u'oï',u'OÏ',u'oá',u'OÁ',u'oà',u'OÀ',u'oå',u'OÅ',u'oã',u'OÃ',u'oä',u'OÄ',u'ôù',u'ÔÙ',u'ôø',u'ÔØ',u'ôû',u'ÔÛ',u'ôõ',u'ÔÕ',u'ôï',u'ÔÏ',    
    u'uù',u'UÙ',u'uø',u'UØ',u'uû',u'UÛ',u'uõ',u'UÕ',u'uï',u'UÏ',u'öù',u'ÖÙ',u'öø',u'ÖØ',u'öû',u'ÖÛ',u'öõ',u'ÖÕ',u'öï',u'ÖÏ',u'yø',u'YØ',u'yû',u'YÛ',u'yõ',u'YÕ',u'î',u'Î',u'yù',u'YÙ'    
]
_KhongDau = [
    u'a',u'A',u'a',u'A',u'd',u'D',u'e',u'E',u'o',u'O',u'o',u'O',u'u',u'U',u'a',u'A',u'a',u'A',u'a',u'A',u'a',u'A',u'a',u'A',
    u'a',u'A',u'a',u'A',u'a',u'A',u'a',u'A',u'a',u'A',u'a',u'A',u'a',u'A',u'a',u'A',u'a',u'A',u'a',u'A',
    u'e',u'E',u'e',u'E',u'e',u'E',u'e',u'E',u'e',u'E',u'e',u'E',u'e','uE',u'e',u'E',u'e',u'E',u'e',u'E',u'i',u'I',u'i',u'I',u'i',u'I',u'i',u'I',u'i',u'I',
    u'o',u'O',u'o',u'O',u'o',u'O',u'o',u'O',u'o',u'O',u'o',u'O',u'o',u'O',u'o',u'O',u'o',u'O',u'o',u'O',u'o',u'O',u'o',u'O',u'o',u'O',u'o',u'O',u'o',u'O',
    u'u',u'U',u'u',u'U',u'u',u'U',u'u',u'U',u'u',u'U',u'u',u'U',u'u',u'U',u'u',u'U',u'u',u'U',u'u',u'U',u'y',u'Y',u'y',u'Y',u'y',u'Y',u'y',u'Y',u'y',u'Y'
    ]

def ConvertEncoding(input_fc, input_fd, sE, dE, caseI):   
    # Define progressor to update progress info
    arcpy.SetProgressor("default")    
    res = arcpy.GetCount_management(input_fc)
    count = int(res.getOutput(0))
    fcount = 0

     #open UpdateCursor on input FC
    rows = arcpy.UpdateCursor(input_fc)
    row = rows.next()
    
    # Loop through each record
    while row:
        #update progressor
        fcount += 1
        progressMessage = "Processing source feature: " + str(fcount) + " of " + str(count)
        arcpy.SetProgressorLabel(progressMessage)
        #newValue = ""
        # read row's value    
        string1 = row.getValue(input_fd)        
        # convert text & update to row
        if  string1.strip() <> "":
            # Convert
            if sE == _VNIWin:
                # Convert VNI-Win to Unicode
                newValue = ConvertVNIWindows(string1)
                # if targerEncode is not Unicode -> Convert to other option
                if dE <> _Unicode:
                    newValue = Convert(newValue,_Unicode,dE)
            else:
                newValue = Convert(string1,sE,dE)
            print newValue
            # Character Case-setting			
            if caseI <> "none":
                newValue = ChangeCase(newValue, caseI)
                print newValue
            # update new value
            row.setValue(input_fd, newValue)
            rows.updateRow(row)
        else:
            row.setValue(input_fd, "")
            rows.updateRow(row)
        row = rows.next() #go to next row in input FC  
    
    arcpy.ResetProgressor()    
    del rows
    del row

def Convert(str,s,d):    
    result = u''
    for c in str:
        if c in s:
            idx = s.index(c)
            if idx >= 0:
                c = d[idx]
        result += c
    return result

def ConvertVNIWindows(txt):
    _VniWindows2= [
        u'aâ',u'AÂ',u'aê',u'AÊ',u'eâ',u'EÂ',u'ô',u'Ô',u'aù',u'AÙ',u'aø',u'AØ',u'aû',u'AÛ',u'aõ',u'AÕ',u'aï',u'AÏ',
        u'aá',u'AÁ',u'aà',u'AÀ',u'aå',u'AÅ',u'aã',u'AÃ',u'aä',u'AÄ',u'aé',u'AÉ',u'aè',u'AÈ',u'aú',u'AÚ',u'aü',u'AÜ',u'aë',u'AË',
        u'eù',u'EÙ',u'eø',u'EØ',u'eû',u'EÛ',u'eõ',u'EÕ',u'eï',u'EÏ',u'eá',u'EÁ',u'eà',u'EÀ',u'eå',u'EÅ',u'eã',u'EÃ',u'eä',u'EÄ',u'ó',u'Ó',u'ò',u'Ò',    
        u'oû',u'OÛ',u'oõ',u'OÕ',u'oï',u'OÏ',u'oá',u'OÁ',u'oà',u'OÀ',u'oå',u'OÅ',u'oã',u'OÃ',u'oä',u'OÄ',u'ôù',u'ÔÙ',u'ôø',u'ÔØ',u'ôû',u'ÔÛ',u'ôõ',u'ÔÕ',u'ôï',u'ÔÏ',    
        u'uù',u'UÙ',u'uø',u'UØ',u'uû',u'UÛ',u'uõ',u'UÕ',u'uï',u'UÏ',u'öù',u'ÖÙ',u'öø',u'ÖØ',u'öû',u'ÖÛ',u'öõ',u'ÖÕ',u'öï',u'ÖÏ',u'yø',u'YØ',u'yû',u'YÛ',u'yõ',u'YÕ',u'yù',u'YÙ',
        u'où',u'OÙ',u'oø',u'OØ',u'oâ',u'OÂ'
    ]
    _VniWindows1= [    
        u'ñ',u'Ñ',u'í',u'Í',u'ì',u'Ì',u'æ',u'Æ',u'ö',u'Ö',u'î',u'Î'    
    ]
    _Unicode2= [
        u'â',u'Â',u'ă',u'Ă',u'ê',u'Ê',u'ơ',u'Ơ',u'á',u'Á',u'à',u'À',u'ả',u'Ả',u'ã',u'Ã',u'ạ',u'Ạ',
        u'ấ',u'Ấ',u'ầ',u'Ầ',u'ẩ',u'Ẩ',u'ẫ',u'Ẫ',u'ậ',u'Ậ',u'ắ',u'Ắ',u'ằ',u'Ằ',u'ẳ',u'Ẳ',u'ẵ',u'Ẵ',u'ặ',u'Ặ',
        u'é',u'É',u'è',u'È',u'ẻ',u'Ẻ',u'ẽ',u'Ẽ',u'ẹ',u'Ẹ',u'ế',u'Ế',u'ề',u'Ề',u'ể',u'Ể',u'ễ',u'Ễ',u'ệ',u'Ệ',u'ĩ',u'Ĩ',u'ị',u'Ị',    
        u'ỏ',u'Ỏ',u'õ',u'Õ',u'ọ',u'Ọ',u'ố',u'Ố',u'ồ',u'Ồ',u'ổ',u'Ổ',u'ỗ',u'Ỗ',u'ộ',u'Ộ',u'ớ',u'Ớ',u'ờ',u'Ờ',u'ở',u'Ở',u'ỡ',u'Ỡ',u'ợ',u'Ợ',    
        u'ú',u'Ú',u'ù',u'Ù',u'ủ',u'Ủ',u'ũ',u'Ũ',u'ụ',u'Ụ',u'ứ',u'Ứ',u'ừ',u'Ừ',u'ử',u'Ử',u'ữ',u'Ữ',u'ự',u'Ự',u'ỳ',u'Ỳ',u'ỷ',u'Ỷ',u'ỹ',u'Ỹ',u'ý',u'Ý',
        u'ó#',u'Ó#',u'ò#',u'Ò#',u'ô#',u'Ô#'
        ]
    _Unicode1= [   
        u'đ',u'Đ',u'í',u'Í',u'ì',u'Ì',u'ỉ',u'Ỉ',u'ư',u'Ư',u'ỵ',u'Ỵ'      
    ]           

    for j in range (0,len(txt)-1):
        c = txt[j:j+2]     
        if c in _VniWindows2:      
            idx = _VniWindows2.index(c)
            if idx >= 0:
                c = _Unicode2[idx]                
            txt = txt.replace(txt[j:j+2],c)

    for j in range (0,len(txt)):
        c = txt[j:j+1]
        if c in _VniWindows1:      
            idx = _VniWindows1.index(c)
            if idx >= 0:
                c = _Unicode1[idx]                
            txt = txt.replace(txt[j:j+1],c)

    for i in range (0,len(txt)):       
        c = txt[i:i+1]  
        if c == u'ó'and txt[i+1:i+2] <> u'#':
            c= u'ĩ'
            txt = txt[:i] + c + txt[i+1:]
        elif c== u'Ó'and txt[i+1:i+2] <> u'#':
            c= u'Ĩ'
            txt = txt[:i] + c + txt[i+1:]
        elif c== u'ò'and txt[i+1:i+2] <> u'#':
            c= u'ị'
            txt = txt[:i] + c + txt[i+1:]
        elif c== u'Ò'and txt[i+1:i+2] <> u'#':
            c= u'Ị'
            txt = txt[:i] + c + txt[i+1:]
        elif c== u'ô'and txt[i+1:i+2] <> u'#':
            c= u'ơ'
            txt = txt[:i] + c + txt[i+1:]
        elif c== u'Ô'and txt[i+1:i+2] <> u'#':
            c= u'Ơ'
            txt = txt[:i] + c + txt[i+1:]

    txt = txt.replace(u'ó#',u'ó')
    txt = txt.replace(u'Ó#',u'Ó')
    txt = txt.replace(u'ò#',u'ò')
    txt = txt.replace(u'Ò#',u'Ò')
    txt = txt.replace(u'ô#',u'ô')
    txt = txt.replace(u'Ô#',u'Ô')
    return txt

def GetEncodeIndex(encodeTxt):
    return{
        "Unicode" : _Unicode,
        "TCVN3" : _TCVN3,
        "VNI-Windows": _VNIWin,
        "Khong dau" : _KhongDau,
    }.get(encodeTxt,_Unicode)

def GetCaseIndex(cText):
	return{
		u'IN HOA' : "upper",
		u'in thường' : "lower",
		u'Hoa đầu câu' : "capitalize",
		u'Hoa Mỗi Từ' : "title",
	}.get(cText, "none")
	
def ChangeCase(str, caseIndex):
	result = u''
	# Character Case-setting
	if caseIndex == "upper":
		result = str.upper()
	elif caseIndex == "lower":
		result = str.lower()
	elif caseIndex == "capitalize":
		result = str.capitalize()
	elif caseIndex == "title":
		result = str.title()
	return result

########################################
#Input parameters
inputFC = arcpy.GetParameterAsText(0)
#inputFC = "D:\\temp\\Test Font\\fontuni.shp"
inputFields = arcpy.GetParameterAsText(1)
#inputFields = "text"
outputFC = arcpy.GetParameterAsText(2)
#outputFC = "D:\\temp\\Test Font\\fontuni2vni.shp"
sourceEncodeTxt = arcpy.GetParameterAsText(3)
#sourceEncodeTxt = "Unicode"
targetEncodeTxt = arcpy.GetParameterAsText(4)
#targetEncodeTxt = "VNI-Windows"
sourceEncode = GetEncodeIndex(sourceEncodeTxt)
targetEncode = GetEncodeIndex(targetEncodeTxt)
#print sourceEncode
#print targetEncode
caseText = arcpy.GetParameterAsText(5)
#caseText = u'IN HOA'
caseIndex = GetCaseIndex(caseText)
#print caseIndex

#Processing block
try:
    #Copy to new feature class
    arcpy.CopyFeatures_management(inputFC,outputFC)
    #Processing conversion of encoding
    inputFL = inputFields.split(";")
    for inputField in inputFL:        
        ConvertEncoding(outputFC, inputField, sourceEncode, targetEncode, caseIndex)
            
    arcpy.AddMessage("Convert from " + sourceEncodeTxt + " to " + targetEncodeTxt)
    arcpy.AddMessage("Finish!")
    print "Finish"
#Free resources
except:
    msgs = arcpy.GetMessage(0)
    msgs +=arcpy.GetMessages(2)
    print msgs
    arcpy.AddError(msgs)
