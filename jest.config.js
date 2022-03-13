// const srcURL = '<rootDir>/matflow/frontend/src/';
const testURL = 'tests/frontendtests/';
const srcURL = '<rootDir>/src/';

module.exports = {
  preset: '@vue/cli-plugin-unit-jest/presets/typescript-and-babel',
  testMatch: ['<rootDir>/tests/frontendtests/**/*.spec.(js|jsx|ts|tsx)'],
  // setupFiles: [`./${testURL}unit/index.ts`],
  moduleNameMapper: {
    '@/(.*)': `${srcURL}/$1`,
    '@Classes/(.*)': `${srcURL}Classes/$1`,
    '@Controler/(.*)': `${srcURL}Controler/$1`,
    '@Memento/(.*)': `${srcURL}Memento/$1`,
    '@Model/(.*)': `${srcURL}Model/$1`,
    '@View/(.*)': `${srcURL}View/$1`,
  },
  transform: {
    '^.+\\.js$': 'babel-jest',
  },
  globals: {
    'ts-jest': {
      diagnostics: false,
    },
  },
};
