import { Keys } from "@Classes/Keys"
import { dataURLtoFile, dataURLtoFileNoMime} from "./base64Utility"

class User {
    private _userName: string
    private _userStatus: string
    private _userPrivilege: string

    /**
    *
    * @param userName The userName
    * @param userStatus The userStatus
    * @param userPrivilege The userPrivilege
    */
    constructor(userName: string, userStatus: string, userPrivilege: string,) {
        this._userName = userName
        this._userStatus = userStatus
        this._userPrivilege = userPrivilege
    }

    /**
    * Gets the userName
    * @returns _userName
    */
    public get userName(): string {
        return this._userName
    }

    /**
    * Gets the userStatus
    * @returns _userStatus
    */
    public get userStatus(): string {
        return this._userStatus
    }

    /**
    * Gets the userPrivilege
    * @returns _userPrivilege
    */
    public get userPrivilege(): string {
        return this._userPrivilege
    }


    /**
    * Sets the value of _userName
    * @param userName The new value of _userName
    */
    public set userName(userName: string) {
        this._userName = userName
    }

    /**
    * Sets the value of _userStatus
    * @param userStatus The new value of _userStatus
    */
    public set userStatus(userStatus: string) {
        this._userStatus = userStatus
    }

    /**
    * Sets the value of _userPrivilege
    * @param userPrivilege The new value of _userPrivilege
    */
    public set userPrivilege(userPrivilege: string) {
        this._userPrivilege = userPrivilege
    }

    /**
    * extracts JSON to User object
    * @param JSONObj The JSON encoded User
    * @returns User object
    * */
    public static createUserObjectFromJSON(JSONObj: string): User {
        const parsed = JSON.parse(JSONObj)
        console.log('parsed ', parsed)
        console.log('username', parsed[Keys.user_name])
        return new User(parsed[Keys.user_name], parsed[Keys.user_status_name], parsed[Keys.user_privilege_name])
    }
}

const jsonString = JSON.stringify({userName: "Soeren", userStatus: "bhceb", userPrivileges: "ndne"})
console.log(jsonString)
User.createUserObjectFromJSON(jsonString)
const encoded1 = "iVBORw0KGgoAAAANSUhEUgAAAHkAAAA9CAYAAACJM8YzAAAAAXNSR0IArs4c6QAAAERlWElmTU0AKgAAAAgAAYdpAAQAAAABAAAAGgAAAAAAA6ABAAMAAAABAAEAAKACAAQAAAABAAAAeaADAAQAAAABAAAAPQAAAAAfV0mUAAADRHRFWHRteGZpbGUAJTNDbXhmaWxlJTIwaG9zdCUzRCUyMmFwcC5kaWFncmFtcy5uZXQlMjIlMjBtb2RpZmllZCUzRCUyMjIwMjItMDItMjJUMDclM0E1NiUzQTU5LjI5NVolMjIlMjBhZ2VudCUzRCUyMjUuMCUyMChNYWNpbnRvc2glM0IlMjBJbnRlbCUyME1hYyUyME9TJTIwWCUyMDEwXzE1XzcpJTIwQXBwbGVXZWJLaXQlMkY2MDUuMS4xNSUyMChLSFRNTCUyQyUyMGxpa2UlMjBHZWNrbyklMjBWZXJzaW9uJTJGMTUuMyUyMFNhZmFyaSUyRjYwNS4xLjE1JTIyJTIwdmVyc2lvbiUzRCUyMjE2LjYuMiUyMiUyMGV0YWclM0QlMjJNSnpJeGRHY09iRlhxR3hjZW4zaCUyMiUyMHR5cGUlM0QlMjJkZXZpY2UlMjIlM0UlM0NkaWFncmFtJTIwaWQlM0QlMjJvOGtVdFlZd1VlM1lFdFJGeEVMeSUyMiUzRWpaSTljNE13RElaJTJGRFR2WXdXM1cwcVJkT2pGMGRySEF2aHJFR1ZPZ3Y3NG1ObCUyQlh5MTBYVG5va0dlbVZJcHJWNDV2aHJmeEFBVG9pc1JnaiUyQmhvUmNqNHg5NTNCNUFFN3BSNVVSZ21QNGczazZoYzhUQmJhS3dGZFlCNVpSRzFWZTRRRk5nMFU5c0M0TVRnYzAwclU0Z0JhWHNFZHlBdXU3JTJCbW5FbFo2JTJCa3llTnY0T3FwTExueE4yOXBHYUw4bGhrazV5Z2NNTzBVdEVNNE5vdlZXUEdlaFp1Nk11MXdmUnRURURqZjFQQWZFRlAxejNZYmJRbDUyV1lRMzJqWUE1UDQ3b3l5Q1ZoYnpseFJ3ZDNIWWRrN2JXemt1Y1dTcXRNOVJvYnJXMExFdFNGSTUzMXVBMzdDS0NmYkdVdVVob0FJeUY4ZUVReVNxTk95bkFHcXlaWEVvb29Hbm9PcHdUallNJTJGYk10SkZzWGxiakVzTUI3dW9WcWYzaVJ6UmxCdGNiZnQzR0s3RTZlWFB3JTNEJTNEJTNDJTJGZGlhZ3JhbSUzRSUzQyUyRm14ZmlsZSUzRXvOLYgAAAEDSURBVHgB7d1REcJAFMXQXQYz9VAdSKmICkJBNVA5MNjYk+cgydzvNz/v13d0Sxt4/um2/VgaUoa7r3M8ZAEKe5GB0kUuMmAAQGzJRQYMAIgtuciAAQCxJRcZMAAgtuQiAwYAxJZcZMAAgNiSiwwYABBbcpEBAwBiSy4yYABAbMlFBgwAiC25yIABALElFxkwACC25CIDBgDEllxkwACA2JKLDBgAEFtykQEDAGJLLjJgAEBsyUUGDACILbnIgAEAsSUXGTAAILbkIgMGAMSWXGTAAIDYkosMGAAQW3KRAQMAYksuMmAAQGzJRQYMAIgtuciAAQCxJRcZMAAgzn41rl/5Bxc7CT0Tte6BAAAAAElFTkSuQmCC"
const encoded = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAHkAAAA9CAYAAACJM8YzAAAAAXNSR0IArs4c6QAAAERlWElmTU0AKgAAAAgAAYdpAAQAAAABAAAAGgAAAAAAA6ABAAMAAAABAAEAAKACAAQAAAABAAAAeaADAAQAAAABAAAAPQAAAAAfV0mUAAADRHRFWHRteGZpbGUAJTNDbXhmaWxlJTIwaG9zdCUzRCUyMmFwcC5kaWFncmFtcy5uZXQlMjIlMjBtb2RpZmllZCUzRCUyMjIwMjItMDItMjJUMDclM0E1NiUzQTU5LjI5NVolMjIlMjBhZ2VudCUzRCUyMjUuMCUyMChNYWNpbnRvc2glM0IlMjBJbnRlbCUyME1hYyUyME9TJTIwWCUyMDEwXzE1XzcpJTIwQXBwbGVXZWJLaXQlMkY2MDUuMS4xNSUyMChLSFRNTCUyQyUyMGxpa2UlMjBHZWNrbyklMjBWZXJzaW9uJTJGMTUuMyUyMFNhZmFyaSUyRjYwNS4xLjE1JTIyJTIwdmVyc2lvbiUzRCUyMjE2LjYuMiUyMiUyMGV0YWclM0QlMjJNSnpJeGRHY09iRlhxR3hjZW4zaCUyMiUyMHR5cGUlM0QlMjJkZXZpY2UlMjIlM0UlM0NkaWFncmFtJTIwaWQlM0QlMjJvOGtVdFlZd1VlM1lFdFJGeEVMeSUyMiUzRWpaSTljNE13RElaJTJGRFR2WXdXM1cwcVJkT2pGMGRySEF2aHJFR1ZPZ3Y3NG1ObCUyQlh5MTBYVG5va0dlbVZJcHJWNDV2aHJmeEFBVG9pc1JnaiUyQmhvUmNqNHg5NTNCNUFFN3BSNVVSZ21QNGczazZoYzhUQmJhS3dGZFlCNVpSRzFWZTRRRk5nMFU5c0M0TVRnYzAwclU0Z0JhWHNFZHlBdXU3JTJCbW5FbFo2JTJCa3llTnY0T3FwTExueE4yOXBHYUw4bGhrazV5Z2NNTzBVdEVNNE5vdlZXUEdlaFp1Nk11MXdmUnRURURqZjFQQWZFRlAxejNZYmJRbDUyV1lRMzJqWUE1UDQ3b3l5Q1ZoYnpseFJ3ZDNIWWRrN2JXemt1Y1dTcXRNOVJvYnJXMExFdFNGSTUzMXVBMzdDS0NmYkdVdVVob0FJeUY4ZUVReVNxTk95bkFHcXlaWEVvb29Hbm9PcHdUallNJTJGYk10SkZzWGxiakVzTUI3dW9WcWYzaVJ6UmxCdGNiZnQzR0s3RTZlWFB3JTNEJTNEJTNDJTJGZGlhZ3JhbSUzRSUzQyUyRm14ZmlsZSUzRXvOLYgAAAEDSURBVHgB7d1REcJAFMXQXQYz9VAdSKmICkJBNVA5MNjYk+cgydzvNz/v13d0Sxt4/um2/VgaUoa7r3M8ZAEKe5GB0kUuMmAAQGzJRQYMAIgtuciAAQCxJRcZMAAgtuQiAwYAxJZcZMAAgNiSiwwYABBbcpEBAwBiSy4yYABAbMlFBgwAiC25yIABALElFxkwACC25CIDBgDEllxkwACA2JKLDBgAEFtykQEDAGJLLjJgAEBsyUUGDACILbnIgAEAsSUXGTAAILbkIgMGAMSWXGTAAIDYkosMGAAQW3KRAQMAYksuMmAAQGzJRQYMAIgtuciAAQCxJRcZMAAgzn41rl/5Bxc7CT0Tte6BAAAAAElFTkSuQmCC"
const file: File = dataURLtoFile(encoded, "bla.drawio")
console.log(file)
const file2: File = dataURLtoFileNoMime(encoded1, "bla.drawio")
console.log(file2)
export default User 