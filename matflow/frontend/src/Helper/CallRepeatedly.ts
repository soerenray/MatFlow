export default function callFunctionRepeatedly(
  // eslint-disable-next-line @typescript-eslint/ban-types
  func: Function,
  numOfRepetions: number,
  delayInMs: number,
) {
  let i = 0;
  const callFunction = window.setInterval(() => {
    func();
    i += 1;
    if (i === numOfRepetions) {
      clearInterval(callFunction);
    }
  }, delayInMs);
}
