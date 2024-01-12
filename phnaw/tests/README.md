# Testing

Triple-A

Arrange, Act, Assert

There is a methodology in unit testing known as Arrange, Act, Assert (abbreviated as AAA):

Arrange: Setup a code environment that mimics the actual environment that your function under test would normally operate in, including any “fake” or “mock” versions of dependencies that the function would normally require.
    
Act: Call the function in this test environment.
    
Assert: When the function under test returns its result, evaluate (by asserting) that the result should be equivalent to something else. If it is, the test passes; if not, the test fails. 