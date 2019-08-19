describe("Active Users", function() {
    it("Active Users", function() {
        // No users
        cy.visit('http://localhost:5000/')
        cy.contains('Active Players:')
        cy.contains('0')

        // 1 user
        cy.get('form').contains('Start Game').click({ force: true })

    })
})