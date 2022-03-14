interface KeyValuePair {
  _keyName: string,
  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  keyValuePairInstance: any,
  keyName: string,
  keyValue: string,
}

class EditKeyValuePairs {
  private _keyValuePairs: Array<KeyValuePair>

  /**
  *
  * @param keyValuePairs The keyValuePairs
  */
  constructor(keyValuePairs: Array<KeyValuePair> = []) {
    this._keyValuePairs = keyValuePairs;
  }

  /**
  * Gets the keyValuePairs
  * @returns _keyValuePairs
  */
  public get keyValuePairs(): Array<KeyValuePair> {
    return this._keyValuePairs;
  }

  /**
  * Sets the value of _keyValuePairs
  * @param keyValuePairs The new value of _keyValuePairs
  */
  public set keyValuePairs(keyValuePairs: Array<KeyValuePair>) {
    this._keyValuePairs = keyValuePairs;
  }

  /**
   * Check's if a keyName is unique in keyValuePairs
   * @param keyValuePairInstance The keyValuePairInstance
   * @param keyName The keyName
   * @returns true if 'keyName' is not used in keyValuePairs, otherwise false
   */
  /* eslint-disable */
  private isKeyUniqueInKeyValuePairs(keyValuePairInstance: any, keyName: string): boolean {
    return ((keyValuePairInstance.keyValuePairs
      .map((keyValuePair: KeyValuePair): string => keyValuePair.keyName)
      .indexOf(keyName) === -1));
  }
  /* eslint-enable */

  /**
   * Adds a new keyValuePair in keyValuePairs
   * @param keyValuePair The keyValuePair
   */
  public addKeyValuePair(keyValuePair: [string, string]) {
    if (this.isKeyUniqueInKeyValuePairs(this, keyValuePair[0])) {
      this._keyValuePairs.push({
        keyValuePairInstance: this,
        _keyName: keyValuePair[0],
        keyValue: keyValuePair[1],
        get keyName(): string {
          return this._keyName;
        },
        set keyName(newKeyName: string) {
          if (this.keyValuePairInstance
            .isKeyUniqueInKeyValuePairs(this.keyValuePairInstance, newKeyName)) {
            this._keyName = newKeyName;
          }
        },
      });
    }
  }
}

export default EditKeyValuePairs;
