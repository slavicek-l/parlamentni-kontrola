// Custom Cypress commands
Cypress.Commands.add('login', (username: string, password: string) => {
  // Custom login command example
})

declare global {
  namespace Cypress {
    interface Chainable {
      login(username: string, password: string): Chainable<void>
    }
  }
}
