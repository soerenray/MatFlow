/**
 * This function converts base64 encoded files to File objects
 * @param dataurl base64 encoded data
 * @param filename of file
 * @returns File object
 */
function dataURLtoFile(dataurl: string, filename: string): File {
  const arr = dataurl.split(',');
  const mineRegex = arr[0].match(/:(.*?);/);
  if (mineRegex == null) {
    throw new Error(`couldn't match regex /:(.*?);/ on ${arr[0]}`);
  }
  const mime = mineRegex[1];
  const bstr = atob(arr[1]);
  let n = bstr.length;
  const u8arr = new Uint8Array(n);

  for (;n > 0; n -= 1) {
    u8arr[n] = bstr.charCodeAt(n);
  }

  return new File([u8arr], filename, { type: mime });
}

/**
 * This function converts base64 encoded files to File objects
 * @param dataurl base64 encoded data
 * @param filename of file
 * @returns File object
 */
function dataURLtoFileNoMime(dataurl: string, filename: string): File {
  const bstr = atob(dataurl);
  let n = bstr.length;
  const u8arr = new Uint8Array(n);

  for (;n > 0; n -= 1) {
    u8arr[n] = bstr.charCodeAt(n);
  }

  return new File([u8arr], filename);
}

/**
 * This function converts File objects to base64 encoded files
 * Implementation taken over from: https://stackoverflow.com/questions/53129002/converting-image-to-base64-string-in-typescript
 * @param file the file object
 * @returns file encoded as string
 */
function fileToDataURL(file: File): string {
  const reader = new FileReader();
  reader.readAsDataURL(file);
  reader.onload = () => reader.result;
  reader.onerror = (error) => {
    // eslint-disable-next-line no-console
    console.log('Error: ', error);
  };
  return ''; // error has occured
}

export { dataURLtoFile, dataURLtoFileNoMime, fileToDataURL };
