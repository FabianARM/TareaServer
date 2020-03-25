
import mimetypes

class request_head_and_get: 
    
    #Mandamos request entera sin partir. 
    def execute(self, request):
        try:
            error = False
            request_split_space = request.split(" ")
            #Buscamos en los archivos de servidor si lo que se nos solicita esta.
            file_name = self.extract_file_name(request_split_space)
            my_file = self.search_file(file_name) 
            if request.find('Accept:') != -1 #si encontramos que si hay encabezado accept
                #-------!lo de arriba es para revisar los accept values.
                #pero ahora es pasar el archivo que le voy a enviar a un mimetype.
                accept_value = mimetypes.guess_type(my_file)

            #Podemos dividir la request en cambios de linea
            request_split_accept = request.split("Accept: ")
            #Ahora recuperamos la linea donde se encuentran los mimetypes.
            request_split_mimetypes = request_split_accept.split('\r\n\r\n')
            
            #Realizamos checkeo de errores. 
            if self.check_error_406(accept_value, request_split_mimetypes):
                error = True
                header = 'HTTP/1.1 406 Not Acceptable\n\n'
                response = '<html><body><center><h3>Error 406: File not Acceptable</h3><p>Servidor AK7</p></center></body></html>'.encode('utf-8')            
            else:
                query_string = self.check_query_string(request_split_space)
                if query_string != " ":
                    response = '<html><body><center><h4>' + query_string + '</h4></center></body></html>'
                    response = response.encode('utf-8')
                    #Procesar query string

            if error: 
                final_response = header
            else:    
                final_response = self.headers_response(my_file, accept_value)
            
            final_response =+ response
            return final_response

        #error 404
        except Exception as e:
            bitacoraLine = ''
            header = 'HTTP/1.1 404 Not Found\n\n'
            response = '<html><body><center><h3>Error 404: File not found</h3><p>Servidor AK7</p></center></body></html>'.encode('utf-8')
    
    #Busca en el servidor el archivo que se le esta solicitando. 
    def search_file(self, request): 
        my_file = request.lstrip('/') # La variable my file contiene el archivo que se esta pidiendo esto se encuentra en la primera linea de la request.
        if(my_file == '')
            my_file = "index.html"
        file = open(my_file,'rb') 
        response = file.read()
        file.close()
        return response

    #Revisa si el archivo que se esta pidiendo esta aceptado o no
    def check_error_406(self, accept_value, accepted_values): 
        if accepted_values.find(accept_value) == -1: #si el valor no esta.
            return True 
         return False

    #Revisa si venia algun parametro con el request.
    def check_query_string(self, request_split):
        if request_split[1].find("?") != -1: #Si encontramos el ?, es que hay parametro. 
            arguments = request_split[1].split("&")
            for element in arguments:
                if element.split("=")[1] != "":
                    query_string = (element.split("=")[1], ) #Enviamos un a tupla con los parametros que el navegador envio.
            return query_string
        return " "
    
    def headers_response(self, requesting_file, accept_value): 
        header = 'HTTP/1.1 200 OK\n'
        header += 'Date: ' + str(datetime.now()) + '\n'
        header += 'Host: ' + str(my_socket.getsockname()[0]) + ':' + str(PORT) + '\n'
        header += 'Server: --->Servidor 100%Real<---\n'
        header += 'Referer: ' + str(my_socket.getsockname()[0]) + ':' + str(PORT) + '\n'
        header += 'Content-Length: ' + str(os.path.getsize(folderRoot + str(requesting_file))) + ' bytes\n'
        header += 'Content-Type: ' + str(accept_value)+'\n\n'
        return header  

    def extract_file_name(self, request_split):
        arguments = request_split.split("?")
        file_name = arguments[0].replace("/", "")
        return file_name