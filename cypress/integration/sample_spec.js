// https://docs.cypress.io/guides/references/trade-offs.html#Multiple-browsers-open-at-the-same-time
// https://docs.cypress.io/api/commands/stub.html#Syntax
// https://docs.cypress.io/guides/guides/stubs-spies-and-clocks.html#Capabilities

describe("Active Users", function() {
  
    it("Active Users", function() {
        // restart server

        cy.request({method: 'POST', url: '/', form : true, json : true, body: { 'restart': true}})

        // No users
        cy.visit('/')
        cy.contains('Active Players:')
        cy.contains('0')

        // 1 user
        cy.get('[name=userName]').type('Jhon')
        cy.get('form').contains('Start Game').click({ force: true })
        cy.wait(2000)
        cy.get('h2').contains('1')
        // 2 user
        cy.request('/board?userName=Jane&size=small&userCookie=1')
            .then((response) => {
                expect(response.body).to.have.property('userCount', 2)
            })

        cy.request('/board?userName=Jane&size=small&userCookie=1&logout=true')
          .then((response) => {
              expect(response.body).to.have.property("userCount", 1)
        })

    })

    it("Push Button 1 user", function() {

        // cy.request('POST', '/', { 'restart': true })
        cy.request({method: 'POST', url: '/', form : true, json : true, body: { 'restart': true, 'debug': true }})
        cy.visit('/')
        cy.get('[name=userName]').type('Jhon')
        cy.get('form').contains('Start Game').click({ force: true })
        // Click
        cy.get('[id=1]').click()
        cy.get('[id=1]').contains('2')
        // Click same button second time
        cy.get('[id=1]').click()
        cy.get('[id=1]').contains('2')
        // Flag
        cy.get('[id=3]').trigger('contextmenu')
        cy.get('[id=3]').contains('F')
        // Don't let click of bomb
        cy.get('[id=3]').click()
        cy.get('[id=3]').contains('F')
        // Unflag
        cy.get('[id=3]').trigger('contextmenu')
        cy.get('[id=3]').click()
        cy.get('[id=3]').contains('1')

        // Click Bomb
        cy.get('[id=0]').click()
        cy.contains('BOOM!')
        cy.contains('Active Players:')
        cy.contains('0')
        
    })
})