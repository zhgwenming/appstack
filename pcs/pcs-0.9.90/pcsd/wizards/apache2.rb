require 'sinatra'
class Apache2Wizard < PCSDWizard

  def long_name
    "HA Apache with Shared Storage 2"
  end
  
  def process_responses
  end

  def collection_page
    out = <<-output_string
<form method=post>
  <table>
    <tr>
      <td colspan=2>
	Configuration a HA Apache 2 web server on top of shared storage:
      </td>
    </tr>
    <tr><td>What is the name of the shared device on all nodes:</td><td><input name="shared_storage_dev" type="text"></td></tr>
    <tr><td>What would you like to name your volume group: </td><td><input type="text" name="vg_name" value="my_vg"></td></tr>
      <tr><td>What would you like to name logical volume: </td><td><input type="text" name="lv_name" value="my_lv"></td></tr>
    <tr><td>What ip address will be shared with all of the nodes: </td><td><input type="text" name="ip_address"></td></tr>
    <tr><td>What is the netmask of the ip address that will be shared (ie. 24): </td><td><input type="text" name="cidr_netmask" value="24"></td></tr>
    <tr><td style="text-align:right" colspan=2><input type=submit></td></tr>
  </table>
</form>
<%= 
PCSDWizard.getchildren
%>
    output_string

    return out
  end

end
