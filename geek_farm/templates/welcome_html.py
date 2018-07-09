# Autogenerated file
def render(stations):
    yield """<div style=\"text-align: center\">
    <img src=\"/static/img/logo.png\" width=\"200\">
</div>
<form name='frmselect' action='/' method=\"post\">
    <table cellpadding='4' border='1' frame='box' rules='all'>
        <TR>
            <TD>Select SSID: <select name='ssid'>
            """
    for wifi in stations:
        yield """            <option value=\""""
        yield str(wifi['ssid'])
        yield """\">"""
        yield str(wifi['ssid'])
        yield """</option>
            """
    yield """            </select>
        <TR>
            <TD>Enter Password for Secured SSID: <input type='password' name='password' maxlength='30' value=''>
        <TR>
            <input class=\"button link\" type='submit' value='Conectar'>
        </TR>
    </table>
</form>
<BR>
<B><U>Available SSID's:</U></B>
<BR>
<table cellpadding='4' border='1' frame='box' rules='all'>
    <TR>
    <TH>SSID
    <TH>Channel
    <TH>Strength
    <TH>Security
    <TH>Visible
    </TR>
    """
    for wifi in stations:
        yield """        <TR>
            <TD>"""
        yield str(wifi['ssid'])
        yield """</TD>
            <TD>"""
        yield str(wifi['channel'])
        yield """</TD>
            <TD>"""
        yield str(wifi['signal'])
        yield """ db</TD>
            <TD>"""
        yield str(wifi['security'])
        yield """</TD>
            <TD>"""
        yield str(wifi['hidden'])
        yield """</TD>
        </TR>
    """
    yield """</table>"""
