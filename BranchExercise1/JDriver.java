/* JDriver.java
   A driver class used for testing utilties.
   e.bonakdarian, Jan 2016
modified be B.R
*/

class JDriver
{
    public static void main(String[] args)
    {
	System.out.println("Testing all utilties\n");

	System.out.println("\nTesting StringUtils");
	// testStringUtils();
	
	System.out.println("\n\n\nTesting ArrayUtils");
	// testArrayUtils();

	System.out.println("\nTesting done by e.bonakdarian");
    }

    public static void testStringUtils()
    {
	String s1 = "Wide open space!";
	StringUtils.spaced_Out(s1);
    }

    public static void testArrayUtils()
    {
	int[] n1 = {1, 2, 3, 4, 5};
	ArrayUtils.print_Vert(n1);
    }
}
