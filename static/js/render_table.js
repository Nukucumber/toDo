function get_tasks_dateline(obj){
    let tasks_dateline = {};
    for (const i in obj) {
        let tasks = obj[i]["tasks"]["task_name"];
        let dateline = obj[i]["tasks"]["dateline"];
        for (let j = 0; j < tasks.length; j++) {
            tasks_dateline[tasks[j] + "." + i] = dateline[j];
        }
    }
    return tasks_dateline;
}

function get_date_diff(date_str){
    let one_day = 1000 * 60 * 60 * 24;
    let date_arr = date_str.split('-');
    let date = new Date(date_arr[0], date_arr[1] - 1, date_arr[2]);
    let curr_date = new Date();

    let date_ms = date.getTime();
    let curr_date_ms = curr_date.getTime();

    let difference_ms = date_ms - curr_date_ms;

    return Math.round(difference_ms/one_day) + 1;
}

function sort_object(obj) {

    let items = Object.keys(obj).map((key) => { 
        return [key, obj[key]];
    });
    
    items.sort((first, second) => { 
        return get_date_diff(first[1]) - get_date_diff(second[1]);
    });
    
    let keys = items.map((e) => { 
        return e[0] 
    });

    let value = items.map((e) => {
        return e[1]
    });

    obj = {};

    for (let i = 0; i < keys.length; i++) {
        obj[keys[i]] = value[i];
    }

    return obj
} 

function date_inc(date_str, inc){
    let one_day = 1000 * 60 * 60 * 24;
    let date_arr = date_str.split('-');
    let date = new Date(new Date(date_arr[0], date_arr[1] - 1, date_arr[2]).getTime() + one_day * inc);
    return (`${date.getFullYear()}-${date.getMonth() + 1}-${date.getDate()}`)
}

function show_add_task_bar(){
    let button = document.getElementById("add_task_button");
    if (button.getAttribute("condition") == undefined || button.getAttribute("condition") == "ADD") {
        button.innerHTML = "-";
        button.setAttribute("condition", "REMOVE")
        document.getElementById("add_task_bar").style.visibility = "visible";
        document.getElementById("add_task_bar").style.position = "static";
        
    }
    else{
        button.innerHTML = "+";
        button.setAttribute("condition", "ADD")
        document.getElementById("add_task_bar").style.visibility = "hidden";
        document.getElementById("add_task_bar").style.position = "absolute";
    }
}

function form_filling(task_cell_id){
    let subject = task_cell_id.split('.')[1];
    let task_name = task_cell_id.split('.')[0];
    let index = data[subject]["tasks"]["task_name"].indexOf(task_name);
    let dateline = data[subject]["tasks"]["dateline"][index];
    let description = data[subject]["tasks"]["description"][index];

    document.querySelector(`#add_task_bar input[name="subject"]`).value = subject;
    document.querySelector(`#add_task_bar input[name="task_name"]`).value = task_name;
    document.querySelector(`#add_task_bar input[name="dateline"]`).value = dateline;
    document.querySelector(`#add_task_bar textarea[name="description"]`).value = description;
}

function render_table(obj, render_date_start, render_date_end){
    let datOfWeek = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
    let date = "";
    if (get_date_diff(render_date_start) < 0){
        render_date_start = new Date();
        render_date_start = `${render_date_start.getFullYear()}-${render_date_start.getMonth() + 1}-${render_date_start.getDate()}`;
        date = render_date_start;
    }
    else{
        date = render_date_start;
    }
    let date_arr = [date];
    let html = "";

    html += `<table class='date_table'>`;
    html += "<tr>";
    html += `
        <th>
            <button id="add_task_button">+</button>
        </th>
    `;
    
    for (let i = 0; i < render_date_end; i++) {
        let tmp = date.split("-"); 
        html += `
            <th>${date}<br> ${datOfWeek[new Date(tmp[0], tmp[1] - 1, tmp[2]).getDay()]}</th>        
        `;
        date = date_inc(date, 1);
        date_arr.push(date);
    }
    html += "</tr>";

    for (const key in obj) {
        let dateline_diff = get_date_diff(obj[key]);
        if (dateline_diff < 0) {
            html += `<tr class="missed">`;
        }
        else if (dateline_diff <= 4 && dateline_diff >= 0) {
            html += `<tr class="urgently">`;
            
        }
        else{
            html += '<tr class="ok">'
        }
        
        html += `
            <td id="${key}" class="task_cell">
                <b>${key}</b>
            </td>        
        `;

        for (let i = 0; i < render_date_end; i++) {
            if (get_date_diff(date_arr[i]) <= dateline_diff) {
                html += `
                    <td class="dateline">
                            
                    </td>        
                `;
            }
            else{
                html += `
                    <td>
    
                    </td>
                
                `;
            }
        }

        html += "</tr>";
    }
    
    html += "</table>";
    html += "<div class='resize_table_input'>"
    html += `<button id="render_date_start_dec">&#8678</button>`;
    
    html += `<button id="render_date_start_inc">&#8680</button>`;
    html += "</div>"

    document.getElementById("landing_tag").innerHTML = html;
    document.getElementById("render_date_start_inc").onclick = function() {
        render_table(
            obj,
            date_inc(render_date_start, 7), 
            render_date_end)
    };
    document.getElementById("render_date_start_dec").onclick = function() {
        render_table(
            obj, 
            date_inc(render_date_start, -7), 
            render_date_end)
    };
    document.getElementById("add_task_button").onclick = function() {
        show_add_task_bar()
    };
    let task_cell = document.getElementsByClassName("task_cell");
    for (let i = 0; i < task_cell.length; i++) {
        task_cell[i].onclick = function() {
            form_filling(task_cell[i].getAttribute("id"));
        }
    }
}


if (Object.keys(data).length != 0){
    console.log(data)
    let tasks_dateline = get_tasks_dateline(data);
    tasks_dateline = sort_object(tasks_dateline);
    let render_date_start =  new Date();
    render_date_start = `${render_date_start.getFullYear()}-${render_date_start.getMonth() + 1}-${render_date_start.getDate()}`
    
    render_table(tasks_dateline, render_date_start, 10);
}