$(function () {
                  var dateField = $('#dateField').datepicker({dateFormat: "yy-mm-dd",minDate:0});
                $(document).ready(function(){

                  $('#btnSave').click(function(event){

                  });

                  $('#btnCancel').click(function(event){
                    // clears form fields and hides the form

                    $('#newForm').addClass('hidden');
                    $('#savedAlert').html("");
                    $('#savedAlert').addClass('hidden');
                    $('#showForm').html('New');
                    $(this).addClass('hidden');
                    clearForm();

                  });

                  $('#showForm').click(function(event){
                    //Shows the new form
                    if( $('#newForm').hasClass('hidden')){
                      $(this).html('Add');
                      $('#newForm').removeClass('hidden');
                      $('#btnCancel').removeClass('hidden');
                    }
                    else{
                      saveAppointment();
                    }
                  });

                  $('#search').click(function(event){
                    var keyword = $('#searchQuery').val();
                    getAppointments(keyword);
                  });


                  function convertFrom24to12(time){
                      var components = time.split(':');
                      var hour = 0 + components[0];
                      var h = hour % 12 || 12;
                      var suffix = hour>12 ? 'PM' : 'AM';

                      return h+":"+components[1]+" "+suffix;


                  }

                  function getAppointments(keyword){
                    if(keyword == undefined){
                      //server url with out keyword returns all
                      keyword = '';
                    }
                    $.ajax({
                      url: '/api/v1.0/'+keyword,
                      type: 'get',
                      success:function(data){
                        if(data.message !=null){
                          $('#searchAlert').html(data.message);
                          $('#searchAlert').removeClass('hidden');
                          $('#appointmentTable').html('');
                        }
                        else{
                          var html = "<tr>"
                                      +"<th>Date</th>"
                                      +"<th>Time</th>"
                                      +"<th>description</th>"
                                      +"</tr>";
                          for(var i =0; i<data.length;i++){
                            var appointment_date = $.datepicker.parseDate("yy-mm-dd",data[i].appointment_time.split(' ')[0]);
                            var month_and_date =$.datepicker.formatDate("MM d",appointment_date);
                            var appointment_time = convertFrom24to12(data[i].appointment_time.split(' ')[1]);
                            html += "<tr>"
                                      +"<td>"+month_and_date+"</td>"
                                      +"<td>"+appointment_time+"</td>"
                                      +"<td>"+data[i].description+"</td>"
                                    +"</tr>";
                                    console.log(data[i]);
                          }
                          console.log(html);
                          $('#appointmentTable').html(html);
                          $('#searchAlert').html("");
                          $('#searchAlert').addClass('hidden');
                        }
                      },
                      error:function(error){

                      }
                    });


                  }

                  function saveAppointment(){
                    // when the save button is clicked
                    var date = $('#dateField').val();
                    try{
                      var time = parseTime($('#timeField').val());
                      console.log(time);
                    }catch(ex){
                      $('#savedAlert').html(ex);
                      $('#savedAlert').removeClass('alert-success');
                      $('#savedAlert').addClass('alert-danger');
                      $('#savedAlert').removeClass('hidden');
                      return;
                    }
                    var description = $('#description').val();
                    //since JSON object is new in ES5 and not all browsers support it and since this is fairly simple to do
                    // i will just concat the strings
                    var data = "{"+
                      '"appointment_time":'+'"'+date+' '+time+'",'+
                      '"description":'+'"'+description+'"'+
                    '}';

                    //send to server
                    // handle response

                    $.ajax({
                        url: '/api/v1.0/',
                        type: 'post',
                        dataType: 'json',
                        contentType: "application/json",
                        success: function (data) {
                          console.log(data);
                            $('#savedAlert').html(data.message);
                            $('#savedAlert').removeClass('alert-danger');
                            $('#savedAlert').addClass('alert-success');
                            $('#savedAlert').removeClass('hidden');
                            clearForm();

                        },
                        error: function(data){
                          //display error on alert div 
                          $('#savedAlert').html("Please make sure you fill all the fields.");
                          $('#savedAlert').removeClass('alert-success');
                          $('#savedAlert').addClass('alert-danger');
                          $('#savedAlert').removeClass('hidden');
                        },
                        data: data
                    });
                  }

                  function clearForm(){
                    $('#dateField').val('');
                    $('#timeField').val('');
                    $('#description').val('');
                  }

                  function parseTime(time){
                    var lower = time.toLowerCase();
                    var twelve = lower.includes('am')||lower.includes('pm');
                    var hour = '';
                    var min = '';
                    lower = lower.trim();

                    console.log(stripped);

                    if(twelve){
                      var stripped = lower.substr(0,lower.length-2).trim();
                      hour = stripped.split(':')[0];
                      min = stripped.split(':')[1];
                      hour =  parseInt(hour);
                      min = parseInt(min);
                      if(hour>12){
                        throw new Error('Hour cannot be greater than 12 is AM/PM is specified');
                      }
                      if(min>59||min<0){
                        throw new Error('Minutes specified are invalid');
                      }
                      if(lower.includes('pm'))
                        hour = 12 + hour;
                    }
                    else{

                      hour = lower.split(':')[0];
                      min = lower.split(':')[1];
                      hour =  parseInt(hour);
                      min = parseInt(min);
                      if(hour>24){
                        throw new Error("Hour cannot be above 24");
                      }
                      if(min>59||min<0){
                        throw new Error('Minutes specified are invalid');
                      }
                    }
                    if(hour <10)
                      hour = "0"+hour;
                    if(min<10)
                      min = "0"+min;
                    return hour+":"+min+":00";
                  }
                });

});
