/* StringUtils.java

   contains some basic string utilities of our own rather than
   using the Java API

   e.bonakdarian, Jan 2016
*/
   

class StringUtils
{
    public static void spaced_Out(String str)
    /* print this string character by character, but with a blank
       space interspersed. E.g., Hello! -> H e l l o !
       No newline is printed.
    */
    {
	System.out.println("** Testing spaced_Out\n");

	for(int i = 0; i < str.length(); i++)
	    System.out.print(str.charAt(i) + " ");
    }
}
