describe('Poslanec Profile', () => {
  it('loads profile page', () => {
    cy.visit('/poslanec/1')
    cy.contains('Návrhy')
  })
})
