//import KeyValuePair from "../Model/KeyValuePair"

interface KeyValuePair {
    _keyName: string,
    keyValuePairInstance: any,
    keyName: string,
    keyValue: string,
}

class KeyValuePairs {
    private _keyValuePairs: Array<KeyValuePair>

    /**
    *
    * @param keyValuePairs The keyValuePairs
    */
    constructor(keyValuePairs: Array<KeyValuePair> = [],) {
        this._keyValuePairs = keyValuePairs
    }

    /**
    * Gets the keyValuePairs
    * @returns _keyValuePairs
    */
    public get keyValuePairs(): Array<KeyValuePair> {
        return this._keyValuePairs
    }

    /**
    * Sets the value of _keyValuePairs
    * @param keyValuePairs The new value of _keyValuePairs
    */
    public set keyValuePairs(keyValuePairs: Array<KeyValuePair>) {
        this._keyValuePairs = keyValuePairs
    }

    private isKeyUniqueInKeyValuePairs(keyValuePairInstance: any, keyName: string,): boolean {
        console.log(keyValuePairInstance)
        return ((keyValuePairInstance.keyValuePairs.map((keyValuePair: KeyValuePair): string => { return keyValuePair.keyName }).indexOf(keyName) === -1) ? true : false)
    }

    public addKeyValuePair(keyValuePair: [string, string]) {
        this._keyValuePairs.push({
            keyValuePairInstance: this,
            _keyName: keyValuePair[0],
            keyValue: keyValuePair[0],
            get keyName(): string {
                return this._keyName
            },
            set keyName(newKeyName: string) {
                if (this.keyValuePairInstance.isKeyUniqueInKeyValuePairs(this.keyValuePairInstance, newKeyName,)) {
                    console.log('changeKey')
                    this._keyName = newKeyName
                }
            },
        })
    }
}

export default KeyValuePairs