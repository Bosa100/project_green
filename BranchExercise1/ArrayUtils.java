/* ArrayUtils.java

   contains some basic string utilities of our own rather than
   using the Java API.

   All array utils MUST work for types int, double, char, String. As
   you implement the 4 versions of each, be sure you put them in this
   order.

   e.bonakdarian, Jan 2016
*/

class ArrayUtils
{
    public static void print_Vert(int[] ar)
    // prints out each element of the supplied array on a separate line
    {
	System.out.println("** Testing print_Vert\n");
	for(int i = 0; i < ar.length; i++)
	    System.out.println(ar[i]);
    }
}
