const testURL = 'tests/frontendtests/'
const srcURL = '<rootDir>/matflow/frontend/src/'

module.exports = {
  preset: '@vue/cli-plugin-unit-jest/presets/typescript-and-babel',
  testMatch: ['<rootDir>/tests/frontendtests/**/*.spec.(js|jsx|ts|tsx)'],  
  setupFiles: ['./' + testURL + "unit/index.ts"],  
  moduleNameMapper: {
    '@Classes/(.*)': srcURL + 'Classes/$1',
    '@Controler/(.*)': srcURL + 'Controler/$1',
    '@Memento/(.*)': srcURL + 'Memento/$1',
    '@Model/(.*)': srcURL + 'Model/$1',
    '@View/(.*)': srcURL + 'View/$1',
  },
  // transformIgnorePatterns: ["/node_modules/"],
  globals: {
    'ts-jest': {
      diagnostics: false
    }
  }
}
