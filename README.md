# Process_Tracker
command line program, which tracks the current running processes

logs can be visualized by the [Process Visualizer](https://max-wittig.github.io/Process_Visualizer/html/)

## install 
1. Install the debian dependency
<pre> # apt install python3-psutil python3-pip </pre>

2. Install the python dependency
<pre> # pip3 install psutil </pre>

3. Run the program
<pre> $ python3 main.py </pre>

4. Let it run and press `ENTER` once you're done

5. Import the log in the [Process Visualizer](https://max-wittig.github.io/Process_Visualizer/html/) and 
enjoy the view

## example visualization

![image](https://user-images.githubusercontent.com/6639323/31406888-42e4c0b4-ae03-11e7-8b62-93d6a7d1851e.png)

## usage

<pre>
usage: Process Tracker [-h] [-l LOAD] [-o OUTPUT] [-i INCLUDED [INCLUDED ...]]
                       [-e EXCLUDED [EXCLUDED ...]] [-b BUILD] [-m]

optional arguments:
  -h, --help            show this help message and exit
  -l LOAD, --load LOAD  Load settings file
  -o OUTPUT, --output OUTPUT
                        Specify output filename
  -i INCLUDED [INCLUDED ...], --included INCLUDED [INCLUDED ...]
                        Set processes that should be tracked
  -e EXCLUDED [EXCLUDED ...], --excluded EXCLUDED [EXCLUDED ...]
                        Set processes that shouldn't be tracked
  -b BUILD, --build BUILD
                        Build settings file, based on current running
                        processes --> excluded_processes
  -m, --manual          Manual input

</pre>