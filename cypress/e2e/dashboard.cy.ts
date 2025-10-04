describe('Dashboard', () => {
  it('loads dashboard page', () => {
    cy.visit('/')
    cy.contains('Top navrhovatelé')
  })
})
