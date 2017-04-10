<!DOCTYPE html>
<html>
<head>
    <title>Laravel</title>

    <link href="https://fonts.googleapis.com/css?family=Lato:100" rel="stylesheet" type="text/css">

    <style>
        html, body {
            height: 100%;
        }

        body {
            margin: 0;
            padding: 0;
            width: 100%;
            display: table;
            font-weight: 100;
            font-family: 'Lato';
        }

        .container {
            text-align: center;
            display: table-cell;
            vertical-align: middle;
        }

        .content {
            text-align: center;
            display: inline-block;
        }

        .title {
            font-size: 96px;
        }
    </style>
</head>
<body>
<div class="container">
    <div class="content">
        <div class="title">Upload XML</div>
        <br>
        @if(Session::has('notif'))
            <h2 style="color: #d58512">{{Session::get('notif')}}</h2>
        @endif
        <br>
        <form action="{{URL::to('xmlupload')}}" method="post" enctype="multipart/form-data">
            <h3>NRP</h3>
            <input type="text" name="nrp" required>
            <br>
            <br>
            <input type="file" name="fileToUpload" id="fileToUpload" required>
            {!! csrf_field() !!}
            <br>
            <br>
            <br>
            <br>
            <input type="submit" value="Hit Me to Upload!!">
        </form>
    </div>
</div>
</body>
</html>
