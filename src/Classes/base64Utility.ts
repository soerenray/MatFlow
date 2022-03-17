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
function fileToDataURLWithFunction(
  file: File,
  func: ((arg1: ArrayBuffer | string, arg2: boolean) => void),
) {
  const reader = new FileReader();
  reader.readAsDataURL(file);
  reader.onload = () => {
    if (reader.result != null) {
      func(reader.result, true);
    }
  };
  reader.onerror = (error) => {
    // eslint-disable-next-line no-console
    console.log('Error: ', error);
  };
}

function filesToDataURLWithFunction(
  files: File[],
  func: ((arg1: [(ArrayBuffer|string), string][], arg2: boolean) => void),
) {
  const filesInBase64WithName: [(ArrayBuffer|string), string][] = [];

  files.forEach((file) => {
    fileToDataURLWithFunction(file, ((input: ArrayBuffer | string) => {
      filesInBase64WithName.push([input, file.name]);
    }));
  });

  let i = 0;
  const lookForFileTransferToComplete = setInterval(() => {
    i += 1;
    console.log('files in base64', filesInBase64WithName.length);
    // Ends if all files are transfered or 50 secconds have passed
    if (filesInBase64WithName.length === files.length || i === 100) {
      func(filesInBase64WithName, true);
      clearInterval(lookForFileTransferToComplete);
    }
  }, 500);
}

export {
  dataURLtoFile, dataURLtoFileNoMime,
  fileToDataURLWithFunction, filesToDataURLWithFunction,
};
