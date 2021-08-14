tpl_dict = {

    'meta_docstring': 'add buttons to toggle input code and output cells',

    'html_header': r"""

<script>
code_show=true;
function code_toggle() {
 if (code_show){
 $('div.input_code').show();
 } else {
 $('div.input_code').hide();
 }
 code_show = !code_show
}
$( document ).ready(code_toggle);
</script>
<script>
output_show=true;
function output_toggle() {
 if (output_show){
 $('div.output_area').show();
 } else {
 $('div.output_area').hide();
 }
 output_show = !output_show
}
$( document ).ready(output_toggle);
</script>

<form action="javascript:code_toggle()" class="input_toggle">
    <input type="submit" value="Toggle Code">
</form>
<form action="javascript:output_toggle()" class="output_toggle">
    <input type="submit" value="Toggle Output">
</form>


<style>
.input_toggle {
  margin: 0 auto;
  width: 90px;
  height: 25px;
  align:center;
  text-align:center;
  position:fixed;
}
.output_toggle {
  margin: 0 auto;
  height: 25px;
  align:center;
  text-align:center;
  position:fixed;
  left:110px;
}
</style>

<!-- If there is a sidebar move it down to accomodate the buttons -->
<style>
.sidebar-wrapper { /* Move down to accomodate button */
	margin-top: 35px;
</style>

<link rel="stylesheet" href="https://code.jquery.com/ui/1.11.4/themes/smoothness/jquery-ui.css">
<script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.9.1/jquery.min.js"></script>


""",

}

# /* To see the limits of the form */
# padding: 1px;
# border: 1px solid #CCC;
# border-radius: 1px;
