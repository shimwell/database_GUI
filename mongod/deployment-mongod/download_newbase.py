

files_complete = []
for f in release_details[args.release]['files']:
    # Establish connection to URL
    url = release_details[args.release]['base_url'] + f
    downloaded_file = download(url)
    files_complete.append(downloaded_file)


ftp://ftp.nrg.eu/pub/www/talys/newbase.tar