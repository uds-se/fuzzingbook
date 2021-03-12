tpl_dict = {

    'meta_docstring': 'with standard nbconvert css layout',

    'html_header': r"""
<title>{{resources['metadata']['name']}}</title>

{% for css in resources.inlining.css -%}
    <style type="text/css">
    {{ css }}
    </style>
{% endfor %}



<style type="text/css">
/* Overrides of notebook CSS for static HTML export */
body {
  overflow: visible;
  padding: 8px;
}

div#notebook {
  overflow: visible;
  border-top: none;
}

{%- if resources.global_content_filter.no_prompt-%}
div#notebook-container{
  padding: 6ex 12ex 8ex 12ex;
}
{%- endif -%}

@media print {
  div.cell {
    display: block;
    page-break-inside: avoid;
  }
  div.output_wrapper {
    display: block;
    page-break-inside: avoid;
  }
  div.output {
    display: block;
    page-break-inside: avoid;
  }
}
</style>

<!-- Custom stylesheet, it must be in the same directory as the html file -->
<link rel="stylesheet" href="custom.css">


""",

    'html_body_start': r"""
   <div tabindex="-1" id="notebook" class="border-box-sizing">
     <div class="container" id="notebook-container">
""",

    'html_body_end': r"""
     </div>
   </div>
"""

}
