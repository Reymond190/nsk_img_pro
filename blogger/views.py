import os
import random
import string

from PIL import Image
from fpdf import FPDF
from PyPDF2 import PdfFileMerger
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
from blogger.models import temp_file_names, db

from blogger import app

ALLOWED_EXTENSIONS = { 'pdf', 'png', 'jpg', 'jpeg', 'gif','heic','tiff','webp'}


def webp_conversion_to_jpg(main_dict):
    '''
        :param main_dict (dict): pass the dict that needs to be modified if success
        :return: dict ,Boolean (true/false) : true if no errors or no webp formats found, false if errors during conversion
        '''
    if 'webp' in main_dict:
        for i in range(0, len(main_dict['webp']['paths'])):
            old_file = main_dict['webp']['paths'][i]
            base_dir = 'temp'  # constant base_dir
            temp_name = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
            filename = secure_filename(temp_name + ".jpeg")

            try:
                im = Image.open(old_file)
                im = im.convert("RGB")
                im.save(os.path.join(base_dir, filename), 'JPEG')
            except Exception as e:
                print('problem in conversion', e)
                return False, main_dict

            final_file_name = base_dir +"/"+ filename
            # delete old file after conversion
            if os.path.isfile(old_file):
                os.remove(old_file)
            else:  ## Show an error ##
                print("Error: %s file not found" % old_file)

            # updating the dictionary
            if 'valid_imgs' in main_dict:
                temp_list = main_dict['valid_imgs']['paths']
                temp_list.append(final_file_name)
                main_dict['valid_imgs']['paths'] = temp_list
                main_dict['valid_imgs']['count'] = main_dict['valid_imgs']['count'] + 1
            else:
                main_dict['valid_imgs'] = {'paths': [final_file_name], 'count': 1}
        end_ = main_dict.pop('webp', None)

        if not end_:  # if cannot delete the key
            print('webp key cannot be removed')
            return False, main_dict
        print('successfully main_dict,updated, and webp file converted to jpeg')
        return True, main_dict
    else:
        return True, main_dict




def gif_conversion_to_jpg(main_dict):
    '''
        :param main_dict (dict): pass the dict that needs to be modified if success
        :return: dict ,Boolean (true/false) : true if no errors or no gif formats found, false if errors during conversion
        '''
    if 'gif' in main_dict:
        for i in range(0, len(main_dict['gif']['paths'])):
            old_file = main_dict['gif']['paths'][i]
            base_dir = 'temp'  # constant base_dir
            temp_name = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
            filename = secure_filename(temp_name + ".jpeg")

            try:
                im = Image.open(old_file)
                mypalette = im.getpalette()
                im.putpalette(mypalette)
                new_im = im.convert("RGB")
                new_im.save(os.path.join(base_dir, filename), 'JPEG')
            except Exception as e:
                print('problem in conversion', e)
                return False, main_dict

            final_file_name = base_dir +'/'+ filename
            # delete old file after conversion
            if os.path.isfile(old_file):
                os.remove(old_file)
            else:  ## Show an error ##
                print("Error: %s file not found" % old_file)

            # updating the dictionary
            if 'valid_imgs' in main_dict:
                temp_list = main_dict['valid_imgs']['paths']
                temp_list.append(final_file_name)
                main_dict['valid_imgs']['paths'] = temp_list
                main_dict['valid_imgs']['count'] = main_dict['valid_imgs']['count'] + 1
            else:
                main_dict['valid_imgs'] = {'paths': [final_file_name], 'count': 1}

        end_ = main_dict.pop('gif', None)

        if not end_:  # if cannot delete the key
            print('gif key cannot be removed')
            return False, main_dict
        print('successfully main_dict,updated, and gif file converted to jpeg')
        return True, main_dict
    else:
        return True, main_dict



def heif_conversion_tojpg(main_dict):           # ONLY SUPPORTED ON LINUX AND MAC
    '''
        :param main_dict (dict): pass the dict that needs to be modified if success
        :return: dict ,Boolean (true/false) : true if no errors or no heif formats found, false if errors during conversion
        '''
    if 'heic' in main_dict:
        for i in range(0, len(main_dict['heic']['paths'])):
            old_file = main_dict['heic']['paths'][i]
            base_dir = 'temp'  # constant base_dir
            temp_name = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
            filename = secure_filename(temp_name+".jpeg")

            try:
                heif_file = pyheif.read(old_file)
                image = Image.frombytes(
                    heif_file.mode,
                    heif_file.size,
                    heif_file.data,
                    "raw",
                    heif_file.mode,
                    heif_file.stride,
                )
                image.save(os.path.join(base_dir,filename), "JPEG")
            except Exception as e:
                print('problem in conversion',e)
                return False,main_dict

            final_file_name = base_dir+'/'+filename
            # delete old file after conversion
            if os.path.isfile(old_file):
                os.remove(old_file)
            else:  ## Show an error ##
                print("Error: %s file not found" % old_file)

            # updating the dictionary
            if 'valid_imgs' in main_dict:
                temp_list = main_dict['valid_imgs']['paths']
                temp_list.append(final_file_name)
                main_dict['valid_imgs']['paths'] = temp_list
                main_dict['valid_imgs']['count'] = main_dict['valid_imgs']['count'] + 1
            else:
                main_dict['valid_imgs'] = {'paths': [final_file_name], 'count': 1}
        end_ = main_dict.pop('heic',None)

        if not end_:        # if cannot delete the key
            print('heic key cannot be removed')
            return False,main_dict
        print('successfully main_dict,updated, and heic file converted to jpeg')
        return True,main_dict
    else:
        return True,main_dict


def tiff_conversion_to_jpeg(main_dict):
    '''
    :param main_dict (dict): pass the dict that needs to be modified if success
    :return: dict ,Boolean (true/false) : true if no errors or no tiff formats found, false if errors during conversion
    '''
    if 'tiff' in main_dict:
        for i in range(0, len(main_dict['tiff']['paths'])):
            old_file = main_dict['tiff']['paths'][i]
            base_dir = 'temp'  # constant base_dir
            temp_name = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
            filename = secure_filename(temp_name+".jpeg")

            try:
                im = Image.open(old_file)
                im = im.convert("RGB")
                im.save(os.path.join(base_dir,filename), 'JPEG')
            except Exception as e:
                print('problem in conversion',e)
                return False,main_dict

            final_file_name = base_dir+'/'+filename
            # delete old file after conversion
            if os.path.isfile(old_file):
                os.remove(old_file)
            else:  ## Show an error ##
                print("Error: %s file not found" % old_file)

            # updating the dictionary
            if 'valid_imgs' in main_dict:
                temp_list = main_dict['valid_imgs']['paths']
                temp_list.append(final_file_name)
                main_dict['valid_imgs']['paths'] = temp_list
                main_dict['valid_imgs']['count'] = main_dict['valid_imgs']['count'] + 1
            else:
                main_dict['valid_imgs'] = {'paths': [final_file_name], 'count': 1}

        end_ = main_dict.pop('tiff',None)

        if not end_:        # if cannot delete the key
            print('tiff key cannot be removed')
            return False,main_dict
        print('successfully main_dict,updated, and tiff file converted to jpeg')
        return True,main_dict
    else:
        return True,main_dict


def convert_images_to_pdf(image_list):
    '''
    :param image_list: list of image paths  ex: [abc/temp.jpg, acd/temp1.jpg]
    :return: Boolean,string True,result_path if pdf created successfully, False if pdf creation failed.
    '''
    pdf = FPDF()
    # imagelist is the list with all image filenames
    base_dir = 'result'
    temp_file = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    result_path = base_dir+'/'+temp_file+'.pdf'
    if not image_list:
        print('list contains not image paths')
        return False,""

    for image in image_list:
        try:
            ratio = 0
            cover = Image.open(image)
            width1, height1 = cover.size
            width, height = float(width1 * 0.264583), float(height1 * 0.264583)
            pdf_size = {'P': {'w': 210, 'h': 297}}
            # get page orientation from image size
            orientation = 'P'
            # make sure image size is not greater than the pdf format size
            width = width if width < pdf_size[orientation]['w'] else None
            height = height if height < pdf_size[orientation]['h'] else None
            print(width, height)
            if width and height:
                pdf.add_page()
                pdf.image(image)
            else:
                print('image width/hieght  larger than pdf')
                max_width = 510   # max size of portrait a4 pdf width in mm (700)
                max_height = 1000    # max size of portrait a4 pdf width in mm (1120)
                width, height = float(width1), float(height1)
                if(width > max_width and height > max_height):
                    ratio1 = max_width / width
                    ratio2 = max_height / height
                    print('ratio1',ratio1,'ratio2',ratio2)
                    ratio = min(ratio1,ratio2)
                    height = height * ratio
                    width = width * ratio
                elif(height > max_height):
                    ratio = max_height / height
                    height = height * ratio
                    width = width * ratio
                elif(width>max_width):
                    ratio = max_width / width
                    height = height * ratio
                    width = width * ratio
                else:
                    print('pdf merger: image size lesser than maxwidth and maxhieght','height',height,'weight',width)
                print('converted',width,height,ratio)
                pdf.add_page()
                mpl = Image.open(image)
                print(mpl.size,'before')
                foo = mpl.resize((round(width), round(height)),Image.ANTIALIAS)
                print(foo.size,'after')
                new_file = ''.join(random.choices(string.ascii_letters + string.digits, k=10))+".jpeg"
                foo = foo.convert('RGB')
                foo.save("temp/"+new_file,quality=100)
                pdf.image("temp/"+new_file)
                print('image size is greater than the pdf size, shrinking the image')
        except Exception as e:
            return False,e       # check before deployment
    pdf.output(result_path, "F")
    return True,result_path


def merge_pdfs(list_pdfs,result_path):
    try:
        merger = PdfFileMerger()
        for pdf in list_pdfs:
            merger.append(pdf)
        merger.write(result_path)
        merger.close()
    except Exception as e:
        print(e)
        return None
    return result_path


def allowed_file(filename):
    print('according to file name extensions',filename.rsplit('.', 1)[1].lower())
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route('/file-upload', methods=['POST'])
def upload_file():
    # check if the post request has the file part
    # if 'file' not in request.files:
    #     resp = jsonify({'message': 'No file part in the request'})
    #     resp.status_code = 400
    #     return resp
    # file = request.files['file']
    temp_dir = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
    files = request.files.getlist('files[]')            # add in form data key:files[]  value:array of files
    print(files)
    file_dict = {}
    #check file
    if not files:
        resp = jsonify({'message': 'No file selected for uploading or wrong key name is used..'})
        resp.status_code = 400
        return resp

    for file in files:
        if file and allowed_file(file.filename):
            filename = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
            filename = secure_filename(filename)
            mimetype  = file.filename.rsplit('.', 1)[1].lower().strip()
            filename = filename+"."+mimetype
            # print('mimetype',mimetype,len(mimetype))
            #store the file names before saving
            bp = temp_file_names('lasd982kjhsadf', 'user-id',mimetype, str(filename),'saved')
            db.session.add(bp)
            db.session.commit()
            if mimetype == 'pdf':
                if 'pdf' in file_dict:
                    temp_list = file_dict['pdf']['paths']
                    temp_list.append('temp/' + filename)
                    file_dict['pdf']['paths'] = temp_list
                    file_dict['pdf']['count'] = file_dict['pdf']['count'] + 1
                else:
                    file_dict['pdf'] = {'paths':['temp/'+filename],'count':1}
            elif mimetype == 'jpg' or  mimetype == 'png' or mimetype == 'jpeg':  # valid img types
                if 'valid_imgs' in file_dict:
                    temp_list = file_dict['valid_imgs']['paths']
                    temp_list.append('temp/'+filename)
                    file_dict['valid_imgs']['paths'] = temp_list
                    file_dict['valid_imgs']['count'] = file_dict['valid_imgs']['count'] + 1
                else:
                    file_dict['valid_imgs'] = {'paths':['temp/'+filename],'count':1}
            elif mimetype == 'heic':
                if 'heic' in file_dict:
                    temp_list = file_dict['heic']['paths']
                    temp_list.append('temp/' + filename)
                    file_dict['heic']['paths'] = temp_list
                    file_dict['heic']['count']  = file_dict['heic']['count'] + 1
                else:
                    file_dict['heic'] = {'paths':['temp/'+filename],'count':1}
            elif mimetype == 'tiff':
                if 'tiff' in file_dict:
                    temp_list = file_dict['tiff']['paths']
                    temp_list.append('temp/' + filename)
                    file_dict['tiff']['paths'] = temp_list
                    file_dict['tiff']['count']  = file_dict['tiff']['count'] + 1
                else:
                    file_dict['tiff'] = {'paths':['temp/'+filename],'count':1}
            elif mimetype == 'webp':
                if 'webp' in file_dict:
                    temp_list = file_dict['webp']['paths']
                    temp_list.append('temp/' + filename)
                    file_dict['webp']['paths'] = temp_list
                    file_dict['webp']['count'] = file_dict['webp']['count'] + 1
                else:
                    file_dict['webp'] = {'paths': ['temp/' + filename], 'count': 1}
            elif mimetype == 'gif':
                if 'gif' in file_dict:
                    temp_list = file_dict['gif']['paths']
                    temp_list.append('temp/' + filename)
                    file_dict['gif']['paths'] = temp_list
                    file_dict['gif']['count'] = file_dict['gif']['count'] + 1
                else:
                    file_dict['gif'] = {'paths': ['temp/' + filename], 'count': 1}
            else:
                print('some new img type found')
            print('file_dict',file_dict)
            # pdf conversion
            file.save(os.path.join('temp', filename))

            # check invalid types and conversion
            # conversion of tiff file formats
        else:
            resp = jsonify({'message': 'Allowed file types are pdf, png, jpg, jpeg, gif, heic, tiff, webp'})
            resp.status_code = 400
            return resp
    # image conversion (.TIFF)
    check,dict = tiff_conversion_to_jpeg(file_dict)
    if check:
        print('tiff imasge conversion success')
        file_dict = dict
    else:
        print('tiff image conversion didnt take place or failed')
    # image conversion (.HEiC)
    # check,dict = heif_conversion_tojpg(file_dict)       # DOES NOT WORK IN WINDOWS
    # if check:
    #     print('heif imasge conversion success')
    #     file_dict = dict
    # else:
    #     print('heif image conversion didnt take place or failed')
    # image conversion (.gif)
    check, dict = gif_conversion_to_jpg(file_dict)
    if check:
        print('gif imasge conversion success',check)
        file_dict = dict
    else:
        print('gif image conversion didnt take place or failed')
    check, dict = webp_conversion_to_jpg(file_dict)
    if check:
        print('webp imasge conversion success',check)
        file_dict = dict
        print(file_dict)
    else:
        print('webp image conversion didnt take place or failed')

    # pdf creation.


    if 'valid_imgs' in file_dict and 'pdf' in file_dict:                 # incase of images and pdfs
        print('both images and pdfs')
        ll, kk = convert_images_to_pdf(file_dict['valid_imgs']['paths'])
        if not ll:
            print('problem in img to pdf conversion',kk)
        else:
            pdfs = file_dict['pdf']['paths']
            end_pdfs = pdfs+[kk]
            dir_name = 'result2'
            temp_file = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
            result_path = merge_pdfs(end_pdfs,dir_name+'/'+temp_file+'.pdf')
            if result_path:
                print('success',result_path)
            else:
                print('problem in pdf merge')
    elif 'pdf' in file_dict: # incase of only pdfs in upload merge them
        print('pdfs only')
        end_pdfs = file_dict['pdf']['paths']
        dir_name = 'result2'
        temp_file = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
        result_path = merge_pdfs(end_pdfs, dir_name + '/' + temp_file + '.pdf')
        if result_path:
            print('success', result_path)
        else:
            print('problem in pdf merge')
    elif 'valid_imgs' in file_dict:  #incase of only imgs without pdfs
        print('images only')
        ll, kk = convert_images_to_pdf(file_dict['valid_imgs']['paths'])
        if not ll:
            print('problem in img to pdf conversion', kk)
        else:
            # pdfs = file_dict['pdf']['paths']
            end_pdfs = [kk]
            dir_name = 'result2'
            temp_file = ''.join(random.choices(string.ascii_letters + string.digits, k=10))
            result_path = merge_pdfs(end_pdfs, dir_name + '/' + temp_file + '.pdf')
            if result_path:
                print('success', result_path)
            else:
                print('problem in pdf merge')
    else:   # if some images cannot be converted to pdfs
        resp = jsonify({'message': 'image formats cannot be converted to pdfs'})
        resp.status_code = 201
        return resp
    resp = jsonify({'message': 'Files successfully uploaded'})
    resp.status_code = 201
    return resp



@app.route('/')
def start_page():
    posts = temp_file_names.query.all()
    files_added = []
    for i in posts:
        print(i.temp_file_name,i.status,i.temp_file_type)
        files_added.append(i)
    print(files_added)
    return 'go to /file-upload'


if __name__ == '__main__':
    app.run()
