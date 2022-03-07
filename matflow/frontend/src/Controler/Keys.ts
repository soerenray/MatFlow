export const keys = {
    userStatusName: "userStatus",
    userPrivilegeName: "userPrivilege",
    passwordName: "password",
    repeatPasswordName: "repeatPassword",
    userName: "userName",
    allUsers: "users",

    templateName: "templateName",
    workflowInstanceName: "workflowInstanceName",
    versionNumberName: "versionNumber",
    versionNoteName: "versionNote",
    configFileName: "configFileName",
    versionsName: "versions",
    frontendVersionsChanges: "parameterChanges",
    keyValuePairsName: "keyValuePairs",

    workflowInstanceNames: "workflowInstanceNames",
    configFileNames: "configFileNames",
    templateNames: "templateNames",
    configFiles: "configFiles",

    namesAndConfigs: "workflowInstanceConfigNames",

    dagPictureName: "dagPicture",
    dagDefinitionName: "dagDefinitionFile",

    statusCodeName: "statusCode",


    serverName: "serverName",
    selectedForExecutionName: "selectedForExecution",
    serverResourcesName: "serverResources",
    serverAddressName: "serverAddress",
    serverStatusName: "serverStatus",
    containerLimitName: "containerLimit",


    tempInName: "temp_in",
    tempOutName: "temp_out",

    filesKey: "file[]",
    fileKey: "file",

    configSavePath: "config",
    dagSavePath: "dag_file",

    underscore: "_",

    oldKey: "oldKey",
    newKey: "newKey",
    oldValue: "oldValue",
    newValue: "newValue",

    // api calls names
    getServerDetails: "/get_server_details",
    setServerDetails: "/set_server_details",
    getAllUsersAndDetails: "/get_all_users_and_details",
    setUserDetails: "/set_user_details",
    deleteUser: "/delete_user",
    getWfInstanceVersions: "/get_wf_instance_versions",
    replaceWfInstanceVersion: "/replace_wf_instance_active_version",
    createVersionOfWfInstance: "/create_version_of_wf_instance",
    getConfigFromWfInstance: "/get_config_from_wf_instance",
    createWfInstance: "/create_workflow_instance",
    getAllWfInstancesNamesAndConfigFileNames: "/get_all_wf_instances_names_and_config_file_names",
    registerUser: "/register_user",
    createTemplate: "/create_template",
    getAllTemplateNames: "/get_all_template_names",
    getTemplate: "/get_template",
    getGraphForTemporaryTemplate: "/get_graph_for_temporary_template",

} as const;